import numpy as np
import trimesh
from trimesh.interfaces.gmsh import load_gmsh
from shapely.geometry import LineString
from pyglet import gl
import matplotlib.pyplot as plt
import cv2

# remove this later , simple png needed
window_conf = gl.Config(double_buffer=True, depth_size=6)


m = trimesh.load_mesh("pyr.stl", enable_post_processing=True, solid=True)

print("Type: {}, centroid:{}".format(type(m), m.centroid))

bounds      = list(m.bounds[0])

h = 0

print(m.bounds)
import sys
#sys.exit()
def save(slice_2D,i):
    #plt.set_aspect('equal')
    fig, ax = plt.subplots(figsize=(16,8))
    ax.set_aspect('equal','datalim')
    # hardcode a format for each entity type
    eformat = {'Line0': {'color': 'g', 'linewidth': 1},
       'Line1': {'color': 'y', 'linewidth': 1},
       'Arc0': {'color': 'r', 'linewidth': 1},
       'Arc1': {'color': 'b', 'linewidth': 1},
       'Bezier0': {'color': 'k', 'linewidth': 1},
       'Bezier1': {'color': 'k', 'linewidth': 1},
       'BSpline0': {'color': 'm', 'linewidth': 1},
       'BSpline1': {'color': 'm', 'linewidth': 1}}
    points = []
    draw_x, draw_y = [],[]
    for entity in slice_2D.entities:
        print(entity,"all attrs here : ",entity.__dict__)
        # if the entity has it's own plot method use it
        #if hasattr(entity, 'plot'):
        #entity.plot(slice_2D.vertices)
        #entity.discrete(slice_2D.vertices)
        #continue

    #unindent if doesn work
        discrete = entity.discrete(slice_2D.vertices)
        # a unique key for entities
        e_key = entity.__class__.__name__ + str(int(entity.closed))
        print("key line etc:",e_key)
        fmt = eformat[e_key].copy()
        if hasattr(entity, 'color') and entity.color != None:
            print("color",entity.color)
        # if entity has specified color use it
            fmt['color'] = entity.color
            plt.plot(*discrete.T, **fmt)
    #plt.plot()
    #plt.savefig(f"mesh_slice_{i}.png")
    #plt.clf()
        draw_x = np.array(slice_2D.vertices[:,0])
        draw_y = np.array(slice_2D.vertices[:,1])
        print("x co-ordinates here",len(slice_2D.vertices[:,0]))
        print("y co-ordinates here",len(slice_2D.vertices[:,1]))
        _ = ax.scatter(slice_2D.vertices[:,0], slice_2D.vertices[:,1], color='lightgray')
        #ax.axis('off')
        #plt.plot(slice_2D.vertices[:,0], slice_2D.vertices[:,1])

    plt.savefig(f'meshx_slice_{i}.png')
    draw_points = (np.asarray([draw_x, draw_y]).T).astype(np.int32)
    img = cv2.imread(f'meshx_slice_{i}.png', 0)
    cv2.polylines(img, [draw_points], False, (0,0,0))
    #plt.show()
    cv2.imshow('image',img)




edges = m.face_adjacency_edges[m.face_adjacency_angles > np.radians(30)]
path = trimesh.path.Path3D(**trimesh.path.exchange.misc.edges_to_path(
        edges, m.vertices.copy()))
scene = trimesh.Scene([m, path])


for i in range(0,34):
    slices = m.section_multiplane(plane_origin=bounds,
                                        plane_normal=[0,0,1],
                                        heights=[h])
    print(h)
    for x in slices:
        #x.show()
        #x.savefig('abcds.png')
        save(x,i)


    h += 0.5
    #png = slices[0].save_image(resolution=[1920, 1080], visible=True, window_conf=window_conf)
    print("Type: {}, centroid: {}".format(type(slices[0]), slices[0].centroid))
