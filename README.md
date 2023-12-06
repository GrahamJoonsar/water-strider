# water-strider
Repository for the code of the Water Strider, WhaleTech's 4th generation robot. For the Mate ROV competition 2023-2024.

## main.py
This file contains the main control loop and combines the function of all the other files. It also controls sending from the laptop to the pi, and displaing the images revieved back.

## onboard.py
This file contains what is running on the raspberry pi inside the robot, making the arduino control the motors and arm along with reading images from the cameras and sending them back up to the surface laptop.

## controls.py
This file reads from the joysticks and converts the data it recieves from them into values for the motors and the arm.

### Author(s)
Graham Joonsar