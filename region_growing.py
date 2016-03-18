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
        
    # create a list of lists of points+neihborhoods as [[point_n, neighbors],[],...]   
    kNN_list = [[] for x in xrange(len(PC))] 
    for point in range(len(PC)):
        # first element in the sublist is the reference point in the neihborhood
        kNN_list[point].append(PC[point])
        neighbors = getNeighbors(PC, PC[point], k)
        # the following elements are the neighbors
        [kNN_list[point].append(i) for i in neighbors]
        
    return kNN_list


