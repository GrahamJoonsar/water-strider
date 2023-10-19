import controls

""" Values for the Robot """
THRUSTERS = {
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

ARM = {
    "TWIST": 1500,
    "TILT":  1500,
    "CLAW":  1500
}

""" Starting the Robot """

controls.init_joysticks()