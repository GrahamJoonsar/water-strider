# The code that is in the raspberry pi, recieving and sending to 
# the arduino and the laptop

from numpysocket import NumpySocket
import threading
import numpy
import serial
import time
import cv2

# Initialize cameras
# Must intialize from greatest to least (idk why)
res_w = 640
res_h = 480

def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 20: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports

#list_ports()

cam0 = cv2.VideoCapture(8)
cam0.set(3, res_w)
cam0.set(4, res_h)
cam1 = cv2.VideoCapture(4)
cam1.set(3, res_w)
cam1.set(4, res_h)
cam2 = cv2.VideoCapture(0)
cam2.set(3, res_w)
cam2.set(4, res_h)

# images
img0 = None
img1 = None
img2 = None
img_hd = None
prev_img = None

check1 = None
check2 = None

currentCamNum = 0
pastCamNum = 0

# Intialize arduino
ard = None
while True:
    try:
        ard = serial.Serial("/dev/ttyACM0", 115200)
        break
    except Exception as e:
        print("CANT CONNECT TO ARDUINO")
        print(e)
        time.sleep(2)

def read_img0():
    global img0, check1
    check1, img0 = cam2.read()
def read_img1():
    global img1, check2
    check2, img1 = cam1.read()
def read_img2():
    global img1, check2
    check2, img1 = cam0.read()
def read_img_hd():
    global img_hd, check, cam0, cam1, cam2
    cam0.release()
    cam1.release()
    cam2.release()
    cam0 = cv2.VideoCapture(8, cv2.CAP_GSTREAMER)
    cam0.set(3, 1920)
    cam0.set(4, 1080)
    check2, img_hd = cam0.read()
    cam0.release()
    cam0 = cv2.VideoCapture(8, cv2.CAP_GSTREAMER)
    cam0.set(3, res_w)
    cam0.set(4, res_h)
    cam1 = cv2.VideoCapture(4, cv2.CAP_GSTREAMER)
    cam1.set(3, res_w)
    cam1.set(4, res_h)
    cam2 = cv2.VideoCapture(0, cv2.CAP_GSTREAMER)
    cam2.set(3, res_w)
    cam2.set(4, res_h)

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
                # Recieving data from the laptop, and parsing it
                data = conn.recv()
                real_data = data[1:int(data[0])+1].tolist()


                get_hd = real_data[-2]

                thread0 = None
                thread1 = None
                if get_hd == 1:
                    thread0 = threading.Thread(target=read_img_hd)
                    thread0.start()
                else:
                    # Starting the threads to gather images from the cameras
                    thread0 = threading.Thread(target=read_img0)
                    thread0.start()
                    thread1 = None
                    if currentCamNum == 1:
                        thread1 = threading.Thread(target=read_img1)
                    else:
                        thread1 = threading.Thread(target=read_img2)
                    thread1.start()

                # Get which camera the pilot wants
                currentCamNum = real_data[-1]

                # write to the arduino (excludes cam num)
                real_bytes = bytearray((str(real_data[:-2]) + ",\n").replace('[', '').replace(']', '').replace(' ', ''), "ascii")
                ard.write(real_bytes)
                print(real_bytes)

                thread0.join()
                if get_hd != 1:
                    thread1.join()
                if get_hd == 1:
                    img = img_hd
                elif check1 and check2:
                    img = cv2.hconcat([img0, img1])
                    prev_img = img
                else:
                    img = prev_img

                try:
                    conn.sendall(img)
                except Exception as e:
                    print("ERROR THING: " + str(e))
                    break
        except ConnectionResetError:
            print("CONNECTION RESET ERROR")
            break
    print("Communication Stopped")

cam0.release()
cam1.release()
cam2.release()