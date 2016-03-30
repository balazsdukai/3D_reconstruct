
import clr
clr.AddReference('mtrand.dll')

import numpy as np
import Rhino as rh
import Grasshopper as gh
import rhinoscriptsyntax as rsyn

# # make dictionary of face_vertex list so that for each vertex the face_ids can be found

# FV_dict = dict()
# #FV_dict['test'] = ['value1']
# #FV_dict['test2'] = ['value2']
# #FV_dict['test2'].append('value3')
# #print FV_dict

# if toggle == True:
    # print "starting indexing vertex-faces topology"
    # num=0
    # for id_face, vertices_ in enumerate(face_vertex):
        # num+=1
        # if (num%1000)==0:
            # print "Processed {} faces".format(str(num))
        # for vertex in vertices_:
            # if FV_dict.has_key(vertex):
                # FV_dict[vertex].add(id_face)
            # else:
                # FV_dict[vertex] = set([id_face])
        # #print id_face
        # #print vertices_
    # print "Finished indexing: {} faces".format(str(num))


# a = FV_dict
# #print type(face_normals[1])
# #print vertices[1]
# #print FV_dict

# # calculate normals for vertices
# # calculate aspect value per vertex
# # slope = normal vector z-axis
# print " "
# print "Start calculation elevation, slope, aspect"
Vertex_attr = [] # vertices with elevation, slope, aspect, id
# num=0
# for vertex_id, vertex in enumerate(vertices):
    # num+=1
    # if (num%1000)==0:
        # print "Processed {} points".format(str(num))
    # Faces_for_vertex = set(FV_dict[vertex_id])
    # List_normals_x = []
    # List_normals_y = []
    # List_normals_z = []
    # for face_id in Faces_for_vertex:
        # List_normals_x.append(face_normals[face_id][0])
        # List_normals_y.append(face_normals[face_id][1])
        # List_normals_z.append(face_normals[face_id][2])
    # mean_x = sum(List_normals_x)/len(List_normals_x)
    # mean_y = sum(List_normals_y)/len(List_normals_y)
    # mean_z = sum(List_normals_z)/len(List_normals_z)
aspect = np.arctan2(mean_x, mean_y)#/np.pi*180
elevation = vertex.Z #z-value Point3D
slope = mean_z
Vertex_attr.append([vertex, elevation, slope, aspect])

# print "Finished indexing: {} points".format(str(num))

b = Vertex_attr
#print b