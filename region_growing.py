import Rhino.Geometry as RG
from collections import deque
import math
import copy

# Create a point dictionary for quick access as: 
# {Reference point(ID): [Ref_geometry(Point3d), Ref_curvature(Float), Ref_normal(Vector3d),[list of neighbors(ID)]]}
PC_dict = dict()
for i in range(len(PC)):
    n_list = []
    for j in PC[i][0][1:]:
        n_list.append(j[1])
    PC_dict[PC[i][0][0][1]] = [PC[i][0][0][0], PC[i][2], PC[i][1], n_list]

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
    aTh: Float. Angle threshold in degrees.
Output:
    R_list: List(Point3d). Region list.    
"""
R_list = [] # Region list
PC_cp = copy.deepcopy(PC_dict)
    
while len(PC_cp) > 0:
    Rc = []
    Sc = []
    Pmin = min(PC_cp, key=PC_cp.get)
    Rc.append(Pmin)
    Sc = deque([Pmin]) # create a queue (FIFO structure)
    print 'Initiated seed list: ' + str(Sc[0])
    while len(Sc) > 0:
        Bc = PC_cp[Sc[0]][3]
        print 'initiated neighbourhood '+str(Bc)+' for seed '+str(Sc[0])
        for j in Bc:
            if PC_cp.has_key(j):
                v1,v2 = PC_cp[Sc[0]][2],PC_cp[j][2]
                # check if angle difference 1.0 indicate identical points
                if RG.Vector3d.VectorAngle(v1, v2) * (180/math.pi) < aTh:
                #if RG.Vector3d.Multiply(v1,v2) > aTh:
                    Rc.append(j) # optionally also append Vector3d
                    if PC_cp[j][1] < cTh:
                        if j not in Sc:
                            Sc.append(j)
                            print str(j)+' added to seed list'
                    #del PC_cp[j]
                    #print str(j)+' deleted from PC_cp'
        print 'removing '+str(Sc[0])+' from PC_cp'
        del PC_cp[Sc[0]]
        print 'removing '+str(Sc[0])+' from seed list'
        Sc.popleft()
        print 'new seed list is: ' + str(Sc)
    R_list.append(Rc)

# output only the point IDs for the respective segment
seg_ID = R_list
# number of segments for quick check
nr_seg = len(R_list)

# output segment-points as Point3d
segment = []
for seg in R_list:
    segment.append([PC_dict[ref_id][0] for ref_id in seg])
seg_3d = segment
