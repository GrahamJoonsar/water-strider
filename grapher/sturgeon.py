import matplotlib.pyplot as plt
 

x =      [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
recv_1 = [5, 3, 2, 1, 0, 1, 1, 3, 0, 2, 3, 4, 2, 1, 0]
recv_2 = [3, 8, 14, 17, 16, 11, 4, 7, 5, 3, 2, 1, 0, 0, 2]
recv_3 = [3, 4, 5, 4, 2, 1, 3, 2, 2, 0, 2, 6, 4, 5, 3]
 
# plotting the points 
plt.plot(x, recv_1, label="Receiver 1")
plt.plot(x, recv_2, label="Receiver 2")
plt.plot(x, recv_3, label="Receiver 3")
 
plt.xlabel('Day')
plt.ylabel('# of sturgeon')

plt.title('Sturgeon Spawning Data')
plt.legend()
plt.show() 