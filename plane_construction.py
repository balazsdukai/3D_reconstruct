import Rhino.Geometry as RG
# Create a point dictionary for quick access as: 
# {Reference point(ID): [Ref_geometry(Point3d), Ref_curvature(Float), Ref_normal(Vector3d),[list of neighbors(ID)]]}
PC_dict = dict()
for i in range(len(PC)):
    n_list = []
    #print PC[i]
    for j in PC[i][0][1:]:
        n_list.append(j[1])
    PC_dict[PC[i][0][0][1]] = [PC[i][0][0][0], PC[i][2], PC[i][1], n_list]

# =======================
# Sort faces from corners and create planes
# =======================
pts = []
pls = []
for segment in seg_ID:
    # segments that have less than 3 points are discarded
    if len(segment) >= 3:
        # Get average curvature of the segment
        cur = [PC_dict[pt][1] for pt in segment]
        cur = sum(cur)/len(cur)
        # If the the avg. curvature is below the threshold, thus it is planar
        # and represents a face not a corner, create a plane.
        if cur < cTh:
            tmp = [PC_dict[pt][0] for pt in segment]
            pl = RG.Plane.FitPlaneToPoints(tmp)[1]
            #o,n = pls.Origin, pls.Normal
            pls.append(pl)
            pts.append(tmp)
        else:
            continue
    else:
        continue

o = len(pls)

planes = pls
points = pts
