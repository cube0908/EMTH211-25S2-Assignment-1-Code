# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 11:23:04 2025


"""

import numpy as np
import matplotlib . pyplot as plt
import time
times = [ ]
sizes = np.arange(0, 5001, 200)
# [... any other setup stuff ...]

colours=['red', 'blue', 'y']
times_collection = [ ]

plt.figure(1)

for i in range(0, 3):
    
    
    times = []
    for n in sizes :
        A = np . random . rand (n , n ) # make a random matrix
        t0a = time . time () # start time
        A@A #No need to assign it to anything
        t1a = time . time () # stop time
        timea = t1a - t0a
        t0b = time . time () # start time
        A@A #No need to assign it to anything
        t1b = time . time () # stop time
        timeb = t1b - t0b
        t0c = time . time () # start time
        A@A #No need to assign it to anything
        t1c = time . time () # stop time
        timec = t1c - t0c
        times . append ( min(timea,timeb, timec) ) # time taken , in seconds
    
    # [... make a glorious plot ! ...]
    plt.plot(sizes, times, color=colours[i])
    times_collection.append(times)
    

plt.title("Time in seconds to compute square of nxn A, as a function of n")
plt.xlabel("Size of square matrix A, n")
plt.ylabel("Time taken to compute A @ A, seconds")


plt.figure(2)


#Taking average of above
averages = []
for i in range(0,len(times)):
    summed = times_collection[0][i] + times_collection[1][i] + times_collection[2][i]
    averages.append(summed/3)
    
plt.plot(sizes, averages, color='m')

#Theoretical time is O(2n**3), or just O(n**3). I'll calculate n**3 up to 5000
#and then take time[-1] and scale such that my final entry == time[-1]
cubes = [ ]
for n in sizes:
    cubes.append(n**3)
#For scaling, we need times[-1] / cubes[-1]; this sneds final item of cubes to
#same value =]
scale = averages[-1] / cubes[-1]
cubes = [cube * scale for cube in cubes]
plt.plot(sizes, cubes, color='green')
plt.title("Average time in seconds to compute square of nxn A, as a function of n")
plt.xlabel("Size of square matrix A, n")
plt.ylabel("Time taken to compute A @ A, seconds")


plt.show()