from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') 
ax.set_aspect('equal')

depth = 36
total_height = 83
total_width = 147
left_width = 25
left_height = 20

right_width = 25
right_height = 25

mid_width = 36

vertices = np.array([
    # Front Face 
    [0, depth, 0], 
    [0, depth, left_height], 
    [left_width, depth, left_height], 
    [left_width, depth, total_height],
    [left_width + mid_width, depth, total_height],
    [left_width + mid_width, depth, right_height],
    [total_width, depth, right_height],
    [total_width, depth, 0],

    # Back Face
    [total_width, 0, 0],
    [total_width, 0, right_height],
    [left_width + mid_width, 0, right_height],
    [left_width + mid_width, 0, total_height],
    [left_width, 0, total_height],
    [left_width, 0, left_height], 
    [0, 0, left_height], 
    [0, 0, 0], 

]) 

pc = Poly3DCollection([vertices])
ax.add_collection3d(pc)

ax.set_xlim([0,250])
ax.set_ylim([0,250])
ax.set_zlim([0,250])
#plotMatrix(ax, ma)
#ax.voxels(ma, edgecolor="k")

plt.show()