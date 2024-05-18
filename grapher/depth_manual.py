import matplotlib.pyplot as plt

depth_values = [0, -0.1, -0.4, -0.9, -1.6, -2.5, -1.6, -0.9, -0.4, -0.1, 0]
time_values = [5*i for i in range(len(depth_values))]

plt.title("Depth over time Graph")
plt.xlabel("Seconds Since Start of Descent")
plt.ylabel("Depth in meters")
plt.plot(time_values, depth_values, "o--r")

plt.show()