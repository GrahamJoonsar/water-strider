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

check1 = None
check2 = None

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

def read_img0():
    global img0, check
    check1, img0 = cam0.read()
def read_img1():
    global img1, check
    check2, img1 = cam1.read()
def read_img2():
    global img1, check
    check2, img1 = cam2.read()

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
                # Starting the threads to gather images from the cameras
                thread0 = threading.Thread(target=read_img0)
                thread0.start()
                thread1 = None
                if currentCamNum == 1:
                    thread1 = threading.Thread(target=read_img1)
                else:
                    thread1 = threading.Thread(target=read_img2)
                thread1.start()


                # Recieving data from the laptop, and parsing it
                data = conn.recv()
                real_data = data[1:data[0]+1].tolist()

                # Get which camera the pilot wants
                currentCamNum = real_data[-1]

                # write to the arduino (excludes cam num)
                real_bytes = bytearray(str(real_data[:-1]).replace('[', '').replace(']', '\n').replace(' ', ''), "ascii")
                ard.write(real_bytes)

                thread0.join()
                thread1.join()
                if check1 and check2:
                    img = cv2.hconcat([img0, img1])
                    prev_img = img
                else:
                    img = prev_img

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