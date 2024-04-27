import pygame, time

# Helpful to convert Joystick to servo values
def map(t, min, max, new_min, new_max):
    return float((new_max - new_min) * (t - min)) / (max - min) + new_min 
 
# Initialize pygame / joysticks
pygame.init()
pygame.joystick.init()

joy1 = None
joy2 = None

def init_joysticks():
    # Attempt to open Joysticks
    global joy1, joy2
    joys = False
    while not joys:
        try:
            joy1 = pygame.joystick.Joystick(0)
            joy2 = pygame.joystick.Joystick(1)
            joys = True
        except:
            print("Failed to connect to Joysticks")
            time.sleep(2)

    # Initialize Joysticks
    joy1.init()
    joy2.init()

# Data input from the controllers
joy1_data = {
    "FB" : 0, 
    "LR" : 0, 
    "TW" : 0, 
    "RE": 0, 
    "CAM_TILT": 0,
    "VERT": 0,
}

joy2_data = {
    "5": 0, 
    "6": 0, 
    "RE": 0, 
    "TW": 0
}

""" Values for the Robot """
prev_thrusters = {
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
    "TILT":  1500,
    "CLAW":  1500
}

misc = {
    "CAM_TILT": 1500,
    "CAM_NUM": 0,
}

# Important Values
fb_weight = 0.4
lr_weight = 0.4
tw_weight = 0.2
deadzone = 0.2
slowdown = 0.5
retain = 0.9


def impose_deadzone(val):
    if abs(val) < deadzone:
        return 0
    else:
        return val

# Buttons
switch_cam_pressed = False
def get_input():
    global switch_cam_pressed
    """ First Controller (Movement) """
    # Horizontal inputs
    joy1_data["LR"] = impose_deadzone(joy1.get_hat(0)[0])
    joy1_data["FB"] = impose_deadzone(joy1.get_axis(1)) # (- = forward, + = backward) 
    joy1_data["TW"] = impose_deadzone(joy1.get_axis(2)) # (- = twist_left, + = twist_right)
    joy1_data["RE"] = -impose_deadzone(joy1.get_axis(3))
    
    # Vertical inputs
    joy1_data["VERT"] = joy1.get_button(4) - joy1.get_button(2)

    # Misc inputs
    joy1_data["CAM_TILT"] = joy1.get_axis(3)

    # Slowdown button pressed
    if joy1.get_button(1) == 1:
        joy1_data["LR"] *= slowdown
        joy1_data["FB"] *= slowdown
        joy1_data["TW"] *= slowdown

    if joy1.get_button(11):
        if not switch_cam_pressed:
            misc["CAM_NUM"] = 1 - misc["CAM_NUM"]
        switch_cam_pressed = True
    else:
        switch_cam_pressed = False

    """ Second Controller (Arm) """
    joy2_data["5"] = joy2.get_button(4)
    joy2_data["6"] = joy2.get_button(5)
    joy2_data["RE"] = -joy2.get_axis(3)
    joy2_data["TW"] = joy2.get_axis(2)

    # For flushing input
    pygame.event.get()

img_pressed = False
def capture_img():
    ret = False
    global img_pressed
    if joy1.get_button(11) == 1:
        if not img_pressed:
            ret = True
        img_pressed = True
    else:
        img_pressed = False
    return ret

def process_input():
    """ Horizontal Thrusters """
    # Omnidirectional Movement
    thrusters["HTL"] = -joy1_data["FB"]*fb_weight + joy1_data["LR"]*lr_weight + joy1_data["TW"]*tw_weight
    thrusters["HTR"] = -joy1_data["FB"]*fb_weight - joy1_data["LR"]*lr_weight - joy1_data["TW"]*tw_weight
    thrusters["HBL"] =  joy1_data["FB"]*fb_weight + joy1_data["LR"]*lr_weight - joy1_data["TW"]*tw_weight
    thrusters["HBR"] =  joy1_data["FB"]*fb_weight - joy1_data["LR"]*lr_weight + joy1_data["TW"]*tw_weight

    # Mapping to Microsencond values
    thrusters["HTL"] = map(thrusters["HTL"], -1, 1, 1000, 2000)
    thrusters["HTR"] = map(thrusters["HTR"], -1, 1, 1000, 2000)
    thrusters["HBL"] = map(thrusters["HBL"], -1, 1, 1000, 2000)
    thrusters["HBR"] = map(thrusters["HBR"], -1, 1, 1000, 2000)

    """ Vertical Thrusters (May need to change to do yaw) """
    thrusters["VTL"] = map(joy1_data["VERT"], -1, 1, 1200, 1800)
    thrusters["VTR"] = map(joy1_data["VERT"], -1, 1, 1200, 1800)
    thrusters["VBL"] = map(joy1_data["VERT"], -1, 1, 1200, 1800)
    thrusters["VBR"] = map(joy1_data["VERT"], -1, 1, 1200, 1800)

    """ Arm steppers (Values should range from -1 to 1) """
    arm["TILT"] = map(joy2_data["RE"], -1, 1, 1000, 1850)
    arm["TWIST"] = map(joy2_data["TW"], -1, 1, 1000, 2000)
    if joy2_data["5"] == 1 and arm["CLAW"] > 1000:
        arm["CLAW"] -= 1
    if joy2_data["6"] == 1 and arm["CLAW"] < 2000:
        arm["CLAW"] += 1

    misc["CAM_TILT"] = map(joy1_data["RE"], -1, 1, 1400, 2100)


def get_send_data():
    for t in prev_thrusters:
        prev_thrusters[t] = prev_thrusters[t]*retain + thrusters[t]*(1-retain)
    send_data = [
        # Arm values
        arm["TILT"], arm["TWIST"], arm["CLAW"],

        # Thruster values
        prev_thrusters["VBL"], prev_thrusters["HBL"], prev_thrusters["VBR"], prev_thrusters["HBR"],
        prev_thrusters["HTR"], prev_thrusters["VTR"], prev_thrusters["HTL"], prev_thrusters["VTL"],
        
        # Other values
        misc["CAM_TILT"], misc["CAM_NUM"],
    ]
    send_data.insert(0, len(send_data))
    return send_data
