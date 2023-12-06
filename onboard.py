# The code that is in the raspberry pi, recieving and sending to 
# the arduino and the laptop

from numpysocket import NumpySocket
import threading
import serial
import time
import cv2

# Initialize cameras
# Must intialize from greatest to least (idk why)
res_w = 320
res_h = 240

cam0 = cv2.VideoCapture(8, cv2.CAP_GSTREAMER)
cam0.set(3, res_w)
cam0.set(4, res_h)
cam1 = cv2.VideoCapture(4, cv2.CAP_GSTREAMER)
cam1.set(3, res_w)
cam1.set(4, res_h)
cam2 = cv2.VideoCapture(0, cv2.CAP_GSTREAMER)
cam2.set(3, res_w)
cam2.set(4, res_h)

# images
img0 = None
img1 = None
img2 = None
prev_img = None

currentCamNum = 1
pastCamNum = 1


# Intialize arduino
ard = None
while True:
    try:
        ard = serial.Serial("/dev/ttyACM0", 9600)
        break
    except Exception as e:
        print("CANT CONNECT TO ARDUINO")
        print(e)
        time.sleep(2)

def process_data():
    pass

def get_view():
    pass

# Main Loop
print("READYY TO CONNECT")
with NumpySocket() as s:
    s.bind(("", 4444))
    while True:
        try:
            s.listen()
            conn, addr = s.accept()
            print("CONNECTED")
            # Main loop
            while conn:
                # Recieving data from the laptop
                data = conn.recv()
                # Parsing the data
                real_data = str(data[0:10].tolist()).replace('[', '').replace(']', '\n').replace(' ', '')
                real_bytes = bytearray(real_data, "ascii")
                
                # Get which camera the pilot wants
                currentCamNum = data[10]

                # write to the arduino
                ard.write(real_bytes)

                img = get_view()
                try:
                    conn.sendall(img)
                except Exception as e:
                    print(e)
                    break
        except ConnectionResetError:
            print("CONNECTION RESET ERROR")
            break
    print("Communication Stopped")

cam0.release()
cam1.release()
cam2.release()