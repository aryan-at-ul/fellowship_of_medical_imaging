import trimesh
import numpy as np
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from trimesh.interfaces.gmsh import load_gmsh
from shapely.geometry import LineString
from pyglet import gl

mesh = trimesh.load_mesh('pyr.stl')

slice = mesh.section(plane_origin=mesh.centroid,
                     plane_normal=[0,0,1])

#slice.show()
def save2(slice_2D,i,k=0):
    slice_2D.show()
    plt.axes().set_aspect('equal', 'datalim')
    # hardcode a format for each entity type
    eformat = {'Line0': {'color': 'g', 'linewidth': 1},
       'Line1': {'color': 'y', 'linewidth': 1},
       'Arc0': {'color': 'r', 'linewidth': 1},
       'Arc1': {'color': 'b', 'linewidth': 1},
       'Bezier0': {'color': 'k', 'linewidth': 1},
       'Bezier1': {'color': 'k', 'linewidth': 1},
       'BSpline0': {'color': 'm', 'linewidth': 1},
       'BSpline1': {'color': 'm', 'linewidth': 1}}
    for entity in slice_2D.entities:
        # if the entity has it's own plot method use it
        if hasattr(entity, 'plot'):
            entity.plot(slice_2D.vertices)
            #continue
        # otherwise plot the discrete curve
        discrete = entity.discrete(slice_2D.vertices)
        # a unique key for entities
        e_key = entity.__class__.__name__ + str(int(entity.closed))

        fmt = eformat[e_key].copy()
        if hasattr(entity, 'color'):
            # if entity has specified color use it
            fmt['color'] = entity.color
        plt.plot(*discrete.T, **fmt)
        plt.savefig(f'meshx_slice_{i}.png',bbox_inches='tight', pad_inches=0)


def save(slice_2D,i,k):
    #plt.set_aspect('equal')
    fig, ax = plt.subplots()

    #fig = plt.figure()
    #fig,ax = plt.subplots()
    #ax = fig.add_axes([0.,0.,1.,1.])
    #ax.set_aspect('equal')
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
    draw_x = np.array(slice_2D.vertices[:,0])
    draw_y = np.array(slice_2D.vertices[:,1])
    _ = ax.scatter(slice_2D.vertices[:,0], slice_2D.vertices[:,1], color='lightgray')
    ax.axis('off')
    #plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
    fig_width, fig_height = plt.gcf().get_size_inches()
    print(i,fig_width, fig_height)
    k = int(k)
    #plt.show()
    plt.savefig(f'/Users/aryansingh/Downloads/images/{i}.png',dpi=k*2)
    plt.close(fig)




slice_2D, to_3D = slice.to_planar()

#slice_2D.show()


z_extents = mesh.bounds[:,2]
# slice every .125 model units (eg, inches)
z_levels  = np.arange(*z_extents, step=.125)


sections = mesh.section_multiplane(plane_origin=mesh.bounds[0],
                                   plane_normal=[0,0,1],
                                   heights=z_levels)

print(z_levels)

#print(sections)
#ax = plt.gca()
i = 0
for s in sections:
#    s.show()
    k = s.area
    print(i,"area",k)
    save2(s,i,k+1)
    i += 1

combined = np.sum(sections)
combined.show()

polygon = slice_2D.polygons_full[0]

#print(polygon)

# intersect line with one of the polygons
hits = polygon.intersection(LineString([[-4,-1], [3,0]]))

print("dddddd",hits)

# check what class the intersection returned
hits.__class__


#ax = plt.gca()
#for h in hits:
#    ax.plot(*h.xy, color='r')
#slice_2D.show()



#(slice_2D + slice_2D.medial_axis()).show()




