
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt 

depth = 36
total_height = 83
total_width = 147
left_width = 25
left_height = 20

right_width = 25
right_height = 25

mid_width = 36

""" Below is one side, so twice this will be the total verticees (16) """
#      +----+
#      |    |
#  +---+    +-------+
#  |                |
#  +----------------+


# Define vertices of the cube 
vertices = np.array([
    # Front Face 
    [0, 0, depth], 
    [0, left_height, depth], 
    [left_width, left_height, depth], 
    [left_width, total_height, depth],
    [left_width + mid_width, total_height, depth],
    [left_width + mid_width, right_height, depth],
    [total_width, right_height, depth],
    [total_width, 0, depth],

    # Back Face
    [0, 0, 0], 
    [0, left_height, 0], 
    [left_width, left_height, 0], 
    [left_width, total_height, 0],
    [left_width + mid_width, total_height, 0],
    [left_width + mid_width, right_height, 0],
    [total_width, right_height, 0],
    [total_width, 0, 0],

]) 


# Visualize the cube mesh 
fig = plt.figure() 
ax = fig.add_subplot(111, projection='3d') 
ax.scatter(vertices[:,0], vertices[:,2], vertices[:,1])

ax.axes.set_xlim3d(left=0, right=250) 
ax.axes.set_ylim3d(bottom=0, top=250) 
ax.axes.set_zlim3d(bottom=0, top=250) 

ax.set_facecolor("Gray")

plt.show()
