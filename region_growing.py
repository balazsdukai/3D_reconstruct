# PC - point cloud
# N - normals
# cTh - curvature threshold
# aTh - angle threshold
# c - curvature estimates

# ==================
# FDN 
# ==================
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
    
# ==================
# kNN
# ==================
def getNeighbors(PC, point, k):
    """
    Calculates the k-Nearest Neighbours(k) for each point(point) in a point cloud(PC)
    Input: 
        PC: Point Cloud as list of points (Point3d)
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
        
    # create a list of lists of points+neihborhoods as [[point_n, neighbors],[],...]   
    kNN_list = [[] for x in xrange(len(PC))] 
    for point in range(len(PC)):
        # first element in the sublist is the reference point in the neihborhood
        kNN_list[point].append(PC[point])
        neighbors = getNeighbors(PC, PC[point], k)
        # the following elements are the neighbors
        [kNN_list[point].append(i) for i in neighbors]
        
    return kNN_list

    
def regionGrowing(PC, N, c, cTh, aTh, nFunction):
    """
    About Rhino GUID in Grasshopper:
    "After any manipulation, of the originally referenced Point from Rhino, it will 
    loose the Guid and subsequently other Rhino informations and it`s pretty hard to 
    find the right guid again. So i would try to keep your Guid from the beginning in 
    your script."
    http://www.grasshopper3d.com/forum/topics/guid-of-an-object
    """
    """
    Region growing algorithm for point cloud segmentation. 
    Implementaion of the algorithm from here:
    http://pointclouds.org/documentation/tutorials/region_growing_segmentation.php
    Input:
        PC: List(Point3d). Point Cloud as list of points.
        N: List(Vector3d). Normal vectors as list of vectors.
        c: List(Float). Curvature estimates for each point.
        cTh: Float. Curvature threshold.
        aTh: Float. Angle threshold.
        nFunction: Function. Neihborhood finding function (kNN or FDN).
    Output:
        R_list: List(?Point3d?). Region list.    
    """
    R_list = [] # Region list
    A = PC[:] # Available point list
    
    while A:
        Rc = []
        Sc = []
        Pmin = 

TODOs:
1. adjust normal calculations so that witch each normal, also the respective point (Point3d) is stored in the list