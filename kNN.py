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
        distances.append((PC[pt], dist, pt))
    # sort the distances in ascending order
    distances.sort(key=operator.itemgetter(1)) 
    neighbors = []
    for x in range(k):
        # retrieve the shortest distance
        neighbors.append((distances[x][0], distances[x][2]))
    return neighbors

# create a list of lists of points+neihborhoods as [[point_n, neighbors],[],...]   
kNN_list = [[] for x in xrange(len(PC))] 
for point in range(len(PC)):
    # first element in the sublist is the reference point in the neihborhood
    #kNN_list[point].append((PC[point],point))
    neighbors = getNeighbors(PC, PC[point], k)
    # the following elements are the neighbors
    [kNN_list[point].append(i) for i in neighbors]
    
a = kNN_list