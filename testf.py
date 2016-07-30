import matplotlib.pyplot as mp
import numpy as np

file = open("ecg.txt","r")
for i in range(0,5000):
    print file.readline()
data = file.read()
'''
fig = mp.figure();

ax1 = fig.add_subplot(111)

ax1.set_title("ECG Plot")
ax1.set_xlabel('Ecg ')
ax1.set_ylabel('time')

data = data.split('\n')

y = [row for row in data]
x = [a for a in range(0,5000)]
y = y[0:5000]
ax1.plot(x,y, c='b', label='the data')

leg = ax1.legend()

mp.show()
'''
#for i in range(0,5000):
