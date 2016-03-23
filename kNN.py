"""
Reference: http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
"""
import clr
clr.AddReference("mtrand")

import math
import operator 
import numpy as np
from numpy import linalg as LA
import Rhino.Geometry as RG

#=========
# Get the k-Nearest Neighbours
#=========

def getNeighbors(PC, point, k):
    """
    Calculates the k-Nearest Neighbours(k) for each point(point) in a point cloud(PC)
    Input: 
        PC: Point Cloud as list of points (Point3d )
        point: a single reference point (Point3d)
        k: number of points in the neihborhood
    Output:
        list: [reference point, pt_1, pt_2, ..., pt_k]
    """
    distances = []
    for pt in range(len(PC)):
        dist = point.DistanceTo(PC[pt])
        distances.append((PC[pt], dist))
    # sort the distances in ascending order
    distances.sort(key=operator.itemgetter(1)) 
    neighbors = []
    for x in range(k):
        # retrieve the shortest distance
        neighbors.append(distances[x][0])
    return neighbors

# create a list of lists of points+neihborhoods as [[point_n, neighbors],[],...]   
kNN_list = [[] for x in xrange(len(PC))] 
for point in range(len(PC)):
    # first element in the sublist is the reference point in the neihborhood
    kNN_list[point].append(PC[point])
    neighbors = getNeighbors(PC, PC[point], k)
    # the following elements are the neighbors
    [kNN_list[point].append(i) for i in neighbors]
    
a = kNN_list

#=======================
# Estimation of normals
#=======================
covM = [] # the list of covariance matrices
point_a = np.empty([len(kNN_list[0]),3]) # a single empty array shaped as an input for the covariance matrix

for Pgroup in range(len(kNN_list)):
    for point in range(len(kNN_list[Pgroup])):
        point_a[point][0] = kNN_list[Pgroup][point][0] # X
        point_a[point][1] = kNN_list[Pgroup][point][1] # Y
        point_a[point][2] = kNN_list[Pgroup][point][2] # Z
        m = np.cov(point_a, rowvar=0) #each column represents a variable, while the rows contain observations
        covM.append(m)

normals = []
for m in range(len(kNN_list)):
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
   x = kNN_list[m][0][0]
   y = kNN_list[m][0][1]
   z = kNN_list[m][0][2]
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