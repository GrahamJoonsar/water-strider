import pygame, time

# Helpful to convert Joystick to servo values
def map(t, min, max, new_min, new_max):
    return float( ((new_max - new_min) * (t - min)) / (max - min) + new_min )

# Initialize pygame / joysticks
pygame.init()
pygame.joystick.init()

joy1 = None
joy2 = None

def init_joysticks():
    # Attempt to open Joysticks
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
    "CAM_TILT": 0
}

joy2_data = {
    "TRIGGER": 0, 
    "RE": 0, 
    "TW": 0
}

""" Values for the Robot """
thrusters = {
    # Horizontal Thrusters
    "HTL": 1500,
    "HTR": 1500,
    "HBL": 1500,
    "HBR": 1500,

    # Vertical Thrusters
    "VTL": 1500,
    "VTR": 1500,
    "VTL": 1500,
    "VTL": 1500
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


def impose_deadzone(val):
    if abs(val) < deadzone:
        return 0
    else:
        return val

# Buttons
switch_cam_pressed = False
def get_input():
    """ First Controller (Movement) """
    joy1_data["LR"] = impose_deadzone(joy1.get_hat(0)[0])
    joy1_data["FB"] = impose_deadzone(joy1.get_axis(1)) # (- = forward, + = backward) 
    joy1_data["TW"] = impose_deadzone(joy1.get_axis(2)) # (- = twist_left, + = twist_right)
    joy1_data["CAM_TILT"] = joy1.get_axis(3)

    # Slowdown button pressed
    if joy1.get_button(1) == 1:
        joy1_data["LR"] *= slowdown
        joy1_data["FB"] *= slowdown
        joy1_data["TW"] *= slowdown

    """ Second Controller (Arm) """
    joy2_data["TRIGGER"] = joy2.get_button(0)
    joy2_data["RE"] = joy2.get_axis(3)
    joy2_data["TW"] = joy2.get_axis(2)

def process_data(img):
    pass

def get_send_data():
    return [
        # Arm values
        arm["TILT"], arm["TWIST"], arm["CLAW"],

        # Thruster values
        thrusters["HTL"], thrusters["HTR"], thrusters["HBL"], thrusters["HBR"],
        thrusters["VTL"], thrusters["VTR"], thrusters["VBL"], thrusters["VBR"], 
        
        # Other values
        misc["CAM_TILT"], misc["CAM_NUM"],
    ]