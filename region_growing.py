
import Rhino.Geometry as RG
# PC - point cloud
# cTh - curvature threshold
# aTh - angle threshold

PC_dict = dict()
for i in range(len(PC)):
    n_list = []
    #print PC[i]
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
    aTh: Float. Angle threshold.
    nFunction: Function. Neihborhood finding function (kNN or FDN).
Output:
    R_list: List(?Point3d?). Region list.    
"""
R_list = [] # Region list

   
while len(PC_dict) > 0:
    Rc = []
    Sc = [] 
    Pmin = min(PC_dict, key=PC_dict.get)
    #Rc.append((*PC_dict[Pmin][0:2]))
    #Sc.append((*PC_dict[Pmin][0:2]))
    Rc.append(Pmin)
    Sc.append(Pmin)
    while len(Sc) > 0:
        for i in range(len(Sc)):
            Bc = PC_dict[Sc[i]][3]
            for j in Bc:
                if PC_dict.has_key(j):
                    #print PC_dict[Sc[i]], PC_dict[j][0]
                    v1,v2 = PC_dict[Sc[i]][2],PC_dict[j][2]
                    # check if angle difference 1.0 indicate identical points
                    if RG.Vector3d.Multiply(v1,v2) > aTh:
                        Rc.append(j) # optionally also append Vector3d
                        if PC_dict[j][1] < cTh:
                            Sc.append(j)
                        del PC_dict[j]
            Sc.pop(i)
    del PC_dict[Pmin]
    R_list.append(Rc)
#print len(R_list)
#print R_list

