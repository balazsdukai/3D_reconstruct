"""  
Just some alternative ideas...
 
for pt in range(len(PC)): 
    RG.Circle(pt, R)
    RG.Curve.Contains(testPoint)
        
create circle with pt as center and R as radius
which points fall into this circle
center point should not be duplicated
"""

import clr
clr.AddReference("mtrand")

import math
import operator 
import numpy as np
from numpy import linalg as LA
import Rhino.Geometry as RG

#=========
# Create Fixed Distance Neighbourhoods
#=========

def getNeighboursInRange(PC, R):
    """
    Get the neighbours in range R
    Input:
        PC: point cloud as list of points (Point3d)
        R: the range/radius (float)
    Output:
        list: list: [reference point, pt_1, pt_2, ..., pt_k]
    """
    # create a list of lists of points+neihborhoods as [[point_n, neighbors],[],...]
    FDN_list = [[] for x in xrange(len(PC))]
    for pt in range(len(PC)):
        p = PC[pt]
        # first element in the sublist is the reference point in the neihborhood
        FDN_list[pt].append(PC[pt])
        neighbours = []
        for p2 in range(len(PC)):
            # calculate distance for each point in PC
            if p.DistanceTo(PC[p2]) < R:
                neighbours.append(PC[p2])
        # the following elements are the neighbors
        [FDN_list[pt].append(i) for i in neighbours]
    return FDN_list

FDN_list = getNeighboursInRange(PC,R)
a = FDN_list

#=======================
# Estimation of normals
#=======================
covM = [] # the list of covariance matrices

for Pgroup in range(len(FDN_list)):
    if len(FDN_list[Pgroup]) <= 1:
        continue
    else:
        point_a = np.empty([len(FDN_list[Pgroup]),3])
        for point in range(len(FDN_list[Pgroup])):
            point_a[point][0] = FDN_list[Pgroup][point][0] # X
            point_a[point][1] = FDN_list[Pgroup][point][1] # Y
            point_a[point][2] = FDN_list[Pgroup][point][2] # Z
            m = np.cov(point_a, rowvar=0)
            if np.isnan(np.sum(m)) or np.isinf(np.sum(m)):
                break
            else:
                #each column represents a variable, while the rows contain observations
                covM.append(m)

normals = []
for m in range(len(FDN_list)):
   # calculate eigenvalues (e_vals) and eigenvectors (e_vecs)
   e_vals, e_vecs = LA.eig(covM[m])
   # get the smallest eigenvalue
   eMin = np.argmin(e_vals)
   # retrieve the smallest eigenvector corresponding to the smallest eigenvalue
   normal = e_vecs[eMin]
   # cast normal coordinates into floats
   normal = [float(i) for i in normal]
   # create a Vector3d from each normal
   # include the respective point for segmentation calculations
   x = FDN_list[m][0][0]
   y = FDN_list[m][0][1]
   z = FDN_list[m][0][2]
   normals.append([RG.Point3d(x,y,z),RG.Vector3d(normal[0],normal[1],normal[2])]) 
#N = normals

#=======================
# Check if the direction of the normals are in align with the point of origin of the LIDAR laser beam
normals_copy = normals[:]
for i in range(len(normals_copy)):
    v = normals_copy[i][1]
    # unitize normals
    v.Unitize()
    # compute dot product of Z unit vector and normal
    dp = RG.Vector3d.Multiply(Z,v) 
    if dp < 0.0:
        # if dot product negative, reverse vector
        normals[i][1].Reverse() 

#=======================
# Estimation of surface curvature
#=======================
curvature = []
for n in normals:
    v = n[1]
    c = v[0]/(v[0]+v[1]+v[2])
    curvature.append([n[0],c],c)
Cur = curvature
