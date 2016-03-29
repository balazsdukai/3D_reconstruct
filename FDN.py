
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
        neighbours = []
        for p2 in range(len(PC)):
            # calculate distance for each point in PC
            if p.DistanceTo(PC[p2]) < R:
                neighbours.append((PC[p2], p2))
        # the following elements are the neighbors
        [FDN_list[pt].append(i) for i in neighbours]
    return FDN_list
   

FDN_list = getNeighboursInRange(PC,R)
print FDN_list[0]
a = FDN_list