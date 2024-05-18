from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from sys import argv

def data_for_cylinder_along_z(center_x,center_y,radius,height_z):
    z = np.linspace(0, height_z, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') 
ax.set_aspect('equal')

depth = float(argv[1]) #36
mid_width = float(argv[2]) #32

total_height = float(argv[3]) #83
total_width = float(argv[4]) #147
left_width = float(argv[5]) #25
left_height = float(argv[6]) #20

right_width = float(argv[7]) #25
right_height = float(argv[8]) #25

front_face = np.array([
    # Front Face 
    [0, depth, 0], 
    [0, depth, left_height], 
    [left_width, depth, left_height], 
    [left_width, depth, total_height],
    [left_width + mid_width, depth, total_height],
    [left_width + mid_width, depth, right_height],
    [total_width, depth, right_height],
    [total_width, depth, 0],
])

back_face = np.array([
    [total_width, 0, 0],
    [total_width, 0, right_height],
    [left_width + mid_width, 0, right_height],
    [left_width + mid_width, 0, total_height],
    [left_width, 0, total_height],
    [left_width, 0, left_height], 
    [0, 0, left_height], 
    [0, 0, 0], 
])

bottom_face = np.array([
    [0, 0, 0],
    [0, depth, 0],
    [total_width, depth, 0],
    [total_width, 0, 0]
])

left_face = np.array([
    [0, 0, 0],
    [0, depth, 0],
    [0, depth, left_height],
    [0, 0, left_height]
])

right_face = np.array([
    [total_width, 0, 0],
    [total_width, depth, 0],
    [total_width, depth, right_height],
    [total_width, 0, right_height]
])

left_top_face = np.array([
    [0, 0, left_height],
    [0, depth, left_height],
    [left_width, depth, left_height],
    [left_width, 0, left_height],
])

right_top_face = np.array([
    [mid_width, 0, right_height],
    [mid_width, depth, right_height],
    [total_width, depth, right_height],
    [total_width, 0, right_height],
])

left_side_face = np.array([
    [left_width, 0, left_height],
    [left_width, depth, left_height],
    [left_width, depth, total_height],
    [left_width, 0, total_height],
])

right_side_face = np.array([
    [left_width + mid_width, 0, right_height],
    [left_width + mid_width, depth, right_height],
    [left_width + mid_width, depth, total_height],
    [left_width + mid_width, 0, total_height],
])

top_face = np.array([
    [left_width, 0, total_height],
    [left_width, depth, total_height],
    [left_width + mid_width, depth, total_height],
    [left_width + mid_width, 0, total_height],
])

pc = Poly3DCollection([front_face, back_face, bottom_face, left_face, right_face, left_top_face, right_top_face, left_side_face, right_side_face, top_face], color="Gray", )
pc.set_edgecolor("Black")
ax.add_collection3d(pc)

Xc,Yc,Zc = data_for_cylinder_along_z(left_width + mid_width/2, depth/2, 8,total_height+25)
ax.plot_surface(Xc, Yc, Zc, alpha=1, color="Pink")

ax.set_xlim([0,250])
ax.set_ylim([0,250])
ax.set_zlim([0,250])

ax.set_title('Width: ' + str(round(total_width, 2)) + "cm\nHeight: " + str(round(total_height, 2)) + "cm", pad=2)

plt.show()