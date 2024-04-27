import matplotlib.pyplot as plt
import serial, time

fresh_density = 997.0474
salty_density = 1023.6
density = fresh_density
g = 9.8

# Intialize arduino
def generate_graph(depth_values):
    global density, g
    pressure_values = [-density*g*float(d)/1000 for d in depth_values]
    time_values = [5*i for i in range(len(depth_values))]

    figure, axis = plt.subplots(2)
    figure.tight_layout(pad=4.0)

    axis[0].set_title("Depth over time Graph")
    axis[0].set_xlabel("Seconds Since Start of Descent")
    axis[0].set_ylabel("Depth in meters")
    axis[0].plot(time_values, depth_values, "o--r")

    axis[1].set_title("Pressure over time Graph")
    axis[1].set_xlabel("Seconds Since Start of Descent")
    axis[1].set_ylabel("Pressure in kilopascals")
    axis[1].plot(time_values, pressure_values, "o--b")

    plt.show()


ard = None
while True:
    try:
        ard = serial.Serial("/dev/ttyACM0", 9600)
        break
    except Exception as e:
        print("CANT CONNECT TO ARDUINO")
        print(e)
        time.sleep(2)

running = True
while running:
    data = ard.readline().replace('\n', '')
    depth_values = [float(val) for val in data.split(sep=',')]
    generate_graph(depth_values)
