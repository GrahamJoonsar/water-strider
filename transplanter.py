"""
Explanatory Paragraph:
The autonomous for tranplanting the brain coral code starts with an image read from the bottom facing camera of the Whale IV. This image is then passed 
through a color filter(red, in this specific case, because the manual specifically said that the square of velcro would be red), and all pixels but the 
specific color of the velcro square are mapped to white, and all other pixels are mapped to black. Then this black and white image is searched for a 
quadrilateral, which would be the velcro square. Using the center of this detected square, we then position the robot directly above it, and lower it 
down onto the square, which successfullytransplants the brain coral to the coral restoration area autonomously.
"""

""" The code below spans across three seperate files, and only the snippets relevant to the autonomous code have been shown """

""" This is the 'transplanter.py' file, it contains the actual autonomous code """

import cv2
import numpy as np
import time


thrusters = {}
arm = {}
misc = {}

# Total amount of time the autonomous will run, 20 seconds
total_time = 20

def reset_values():
    global thrusters, arm, misc
    thrusters = {
        # Horizontal Thrusters
        "HTL": 1500,
        "HTR": 1500,
        "HBL": 1500,
        "HBR": 1500,

        # Vertical Thrusters
        "VTL": 1500,
        "VTR": 1500,
        "VBL": 1500,
        "VBR": 1500
    }

    arm = {
        "TWIST": 1500,
        "TILT":  1700,
        "CLAW":  1500
    }

    misc = {
        "CAM_TILT": 1500,
        "CAM_NUM": 1,
        "TAKE_PICTURE": 0,
    }

start_time = 0
def intialize_autonomous():
    global start_time
    reset_values()
    start_time = time.time()

# Helper function that isolates the color of the transplanting site in the camera feed
def isolate_color(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    mask = mask0+mask1

    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    output_img[np.where(mask!=0)] = 1
    return output_img

# Locates a quadrilateral in an image
def maxl(l): return l.index(max(l))
def find_rect(i_inp):
    i_gray = cv2.cvtColor(i_inp, cv2.COLOR_BGR2GRAY)
    i_blur = cv2.GaussianBlur(i_gray, (11, 11), 0)
    i_bin = cv2.threshold(i_blur, 60, 255, cv2.THRESH_BINARY)[1]

    i_2, contours, hierarchy = cv2.findContours(i_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt_largest_i = maxl(list(cv2.contourArea(c) for c in contours))
    cnt_largest = contours[cnt_largest_i]

    epsilon = 0.02 * cv2.arcLength(cnt_largest, True)
    approx = cv2.approxPolyDP(cnt_largest, epsilon, True)

    return approx

def get_send_data(img):
    masked_img = isolate_color(img) # image with white where the specific color is and black elsewhere
    t_area_cnt = find_rect(masked_img) # The contour associated with the
    
    # center of the transplantation area
    M = cv2.moments(t_area_cnt)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    ## Setting the motor values
    if abs(cx-img.shape[1]//2) + abs(cy-img.shape[0]//2) < 10: # If approximately centered
        # No need to move horizontally
        thrusters["HTL"] = 1500
        thrusters["HTR"] = 1500
        thrusters["HBL"] = 1500
        thrusters["HBR"] = 1500

        # Slowly descend onto the transplantation area
        thrusters["VTL"] = 1400
        thrusters["VTR"] = 1400
        thrusters["VBL"] = 1400
        thrusters["VBR"] = 1400
    else: # Not centered above the transplantation area
        fb_val = 0.5 if cy < img.shape[0]//2 else 0 # move the robot forward until the T-site is below
        lr_val = cx/(img.shape[1]//2) - 1 # center the robot horizontally

        thrusters["HTL"] = -fb_val*0.4 + lr_val*0.4
        thrusters["HTR"] = -fb_val*0.4 - lr_val*0.4
        thrusters["HBL"] =  fb_val*0.4 + lr_val*0.4
        thrusters["HBR"] =  fb_val*0.4 - lr_val*0.4

        # Map to microsecond values
        thrusters["HTL"] = map(thrusters["HTL"], -1, 1, 1000, 2000)
        thrusters["HTR"] = map(thrusters["HTR"], -1, 1, 1000, 2000)
        thrusters["HBL"] = map(thrusters["HBL"], -1, 1, 1000, 2000)
        thrusters["HBR"] = map(thrusters["HBR"], -1, 1, 1000, 2000)

        # Ascend to a higher FOV
        thrusters["VTL"] = 1650
        thrusters["VTR"] = 1650
        thrusters["VBL"] = 1650
        thrusters["VBR"] = 1650

    finished = int(time.time() - start_time > total_time)
    send_data = [
        # Arm values
        arm["TILT"], arm["TWIST"], arm["CLAW"],

        # Thruster values
        thrusters["VBL"], thrusters["HBL"], thrusters["VBR"], thrusters["HBR"],
        thrusters["HTR"], thrusters["VTR"], thrusters["HTL"], thrusters["VTL"],
        
        # Other values
        misc["CAM_TILT"], misc["TAKE_PICTURE"], misc["CAM_NUM"],
    ]
    send_data.insert(0, len(send_data))
    send_data.append(finished)
    return send_data