"""
Author(s): Graham Joonsar, 

Run pi code first, then here

This is the code for the surface laptop.

RPI Password:
 - password
    
SSH into RPI:
 - ssh pi@raspberrypi.local
 - cd Desktop/code
 - python3 control.py

"""

# External Libs
from numpysocket import NumpySocket
import numpy
import cv2

# Internal libs
import controls

""" Starting the Robot """

controls.init_joysticks()

# Clear screen and set cursor to the top right
print("\033[?25l")
print("\033[2J")

# Establishing Connection and Main Loop
port = 4444
host = "raspberrypi.local"
with NumpySocket() as sock:
    # Attempt Connection
    sock.connect((host, port))

    # Main code loop
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()