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

