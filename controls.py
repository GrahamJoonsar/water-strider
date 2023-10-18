import pygame, time

# Initialize pygame / joysticks
pygame.init()
pygame.joystick.init()

joy1 = None
joy2 = None

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