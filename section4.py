import trimesh
import numpy as np
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from trimesh.interfaces.gmsh import load_gmsh
from shapely.geometry import LineString
from pyglet import gl
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
from scipy import stats
import cv2
import os
from PIL import Image,ImageOps

mesh = trimesh.load_mesh('pyr.stl')

slice = mesh.section(plane_origin=mesh.centroid,
                     plane_normal=[0,0,1])



def save2(slice_2D,i,k=0):
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
            continue
        # otherwise plot the discrete curve
        discrete = entity.discrete(slice_2D.vertices)
        # a unique key for entities
        e_key = entity.__class__.__name__ + str(int(entity.closed))

        fmt = eformat[e_key].copy()
        if hasattr(entity, 'color'):
            # if entity has specified color use it
            fmt['color'] = entity.color
        plt.plot(*discrete.T, **fmt)
        plt.axis('off')
        #plt.savefig(f'meshx_slice_{i}.png',bbox_inches='tight', pad_inches=0)
        plt.savefig(f'/Users/aryansingh/Downloads/images/{i}.png',dpi=int(line[i])*2,bbox_inches='tight', pad_inches=0)
    plt.clf()
        #add_background(path,imgnm)


def add_background():

    path = "/Users/aryansingh/Downloads/images"
    files = os.listdir(path)
    for x in files:
        print(x)
        img = Image.open(f'{path}/{x}','r')
        img = ImageOps.grayscale(img)
        img_w, img_h = img.size
        background = Image.new('RGBA', (1440, 900), (255, 255, 255, 255))
        bg_w, bg_h = background.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        background.paste(img, offset)
        background.save(f'{path}/{x}')


def save3(slice_2D,i,k=0):
    #slice_2D.show()
    plt.axes().set_aspect('equal', 'datalim')
    # hardcode a format for each entity type
    #plt.rcParams.update({'figure.autolayout': True})
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
            continue
        # otherwise plot the discrete curve
        discrete = entity.discrete(slice_2D.vertices)
        # a unique key for entities
        e_key = entity.__class__.__name__ + str(int(entity.closed))

        fmt = eformat[e_key].copy()
        if hasattr(entity, 'color'):
            # if entity has specified color use it
            fmt['color'] = entity.color
        plt.axis('off')
        plt.plot(*discrete.T, **fmt)
        plt.savefig(f'meshx_slice_{i}.png',bbox_inches='tight', pad_inches=0)
        #plt.savefig(f'/Users/aryansingh/Downloads/images/{i}.png',dpi=int(line[i])*2,bbox_inches='tight', pad_inches=0)
        plt.clf()



line = []
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
    plt.savefig(f'/Users/aryansingh/Downloads/images/{i}.png',dpi=int(line[i])*2)
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

x,y = [],[]
for s in range(len(sections)):
    x.append(s)
    y.append(sections[s].area)




slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

line = slope*np.array(x)+intercept
plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(slope,intercept))
#end

plt.scatter(x,y, color="k", s=3.5)
plt.legend(fontsize=9)


print("here is the min:",min(line))

print("==============================")
print(line)
print("==============================")

add = abs(min(line)) + 1
print("added to min",add)
line = [x + add for x in line]
print(line)



#plt.show()





import sys

for s in sections:
#    s.show()
    k = s.area
    print(i,"area",line[i])
    save2(s,i,k+1)
    i += 1


add_background()

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




