"""
Companies choosing to transplant the brain coral autonomously are tasked with creating software that
will allow their vehicle to autonomously transplant the brain coral from the nursery area to the coral
restoration area. Companies that successfully transplant brain coral using an autonomous control
program will receive 30 points. Successfully transplanting the brain coral autonomously is defined as
the control program moving the vehicle from the coral nursery to the coral restoration area and placing
the brain coral on the red Velcro square. Any portion of the bottom of the brain coral may be touching
any portion of the red Velcro square. During transplantation, no company member should be touching
the controls or other systems. The pilot may manually pick up the brain coral from the coral nursery,
but once the brain coral is no longer in contact with the nursery, all movement of the vehicle must be
autonomous. A tether manager may hold the tether but cannot guide the vehicle in any way.
Companies attempting to transplant the brain coral autonomously should inform the station judge that
they are doing so prior to picking up the brain coral. If a company cannot successfully transplant the
brain coral onto the Velcro square, they may attempt to do so manually. Companies will get one
attempt at performing the task autonomously. If at any time after picking up the brain coral the
company must take manual control, they cannot get points for autonomous transplanting. Companies
should inform the station judge when they switch to manual transplanting of the brain coral.
"""

import cv2
import numpy as np

def isolate_red(img):
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
    return output_img

#cam = cv2.VideoCapture(0)
#while True:
#    ret, img = cam.read()
#if not ret:
#    print("failed to grab frame")
#    break
img = cv2.imread("autonomous/image.png")
red_img = isolate_red(cv2.GaussianBlur(img,(5,5),0)) 
gray = cv2.cvtColor(red_img, cv2.COLOR_BGR2GRAY) 
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
for i in range(1, len(contours)):
    approx = cv2.approxPolyDP(contours[i], 0.01 * cv2.arcLength(contours[i], True), True)
    if True or len(approx) == 4:
        cv2.drawContours(red_img, [contours[i]], 0, (0, 255, 0), 5) 
cv2.imshow("test", red_img)
while True:
    k = cv2.waitKey(1)