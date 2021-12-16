#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 17:44:29 2021

@author: tylerpruitt
"""

import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

def eulerStep(x, y, Vx, Vy, Ax, Ay, dt):
    '''Function takes in positions, velocities, accelerations, and dt as inputs
    returns the newly calculated postions and velocities'''
    for i in range(3):
        x[i] += Vx[i] * dt
        y[i] += Vy[i] * dt
        
        Vx[i] += Ax[i] * dt
        Vy[i] += Ay[i] * dt
    
    return x, y, Vx, Vy

def computeAcceleration(masses, x, y):
    '''Function takes in masses and initial positions as inputs
    returns the instantaneous gravitational accelerations of each mass'''
    
    # Initialize the x an y distances between the three objects
    x12 = x[1] - x[0]
    x13 = x[2] - x[0]
    x23 = x[1] - x[0]
    
    # Compute the distances between the objects
    y12 = y[1] - y[0]
    y13 = y[2] - y[0]
    y23 = y[1] - y[0]
    
    r12 = np.sqrt(x12**2 + y12**2)
    r13 = np.sqrt(x13**2 + y13**2)
    r23 = np.sqrt(x23**2 + y23**2)
    
    Ax, Ay = [], []
    
    # Compute the accelerations for objects 1, 2, and 3
    Ax.append(x12 * masses[1] / r12**3 + x13 * masses[2] / r13**3)
    Ay.append(y12 * masses[1] / r12**3 + y13 * masses[2] / r13**3)
    
    Ax.append(-x12 * masses[0] / r12**3 + x23 * masses[2] / r23**3)
    Ay.append(-y12 * masses[0] / r12**3 + y23 * masses[2] / r23**3)
    
    Ax.append(-x13 * masses[0] / r13**3 - x23 * masses[1] / r23**3)
    Ay.append(-y13 * masses[0] / r13**3 - y23 * masses[1] / r23**3)
    
    return Ax, Ay

# Initialize starting conditions (masses, speeds, and positions)
# 0: Sun, 1: Earth, 2: Moon
masses, Vx, Vy, x, y = [], [], [], [], []

print("Enter the masses for the Sun (3.0), Earth (0.01), and Moon(0.0001)")
masses.append(float(input("Sun's mass: ")))
masses.append(float(input("Earth's mass: ")))
masses.append(float(input("Moon's mass: ")))

print("Enter the three inital x velocities (0, 0, 0)")
Vx.append(float(input("Sun's initial x velocity: ")))
Vx.append(float(input("Earth's initial x velocity: ")))
Vx.append(float(input("Moon's initial x velocity: ")))

print("Enter the three inital y velocities (0, 0.5477, 0.6891)")
Vy.append(float(input("Sun's initial y velocity: ")))
Vy.append(float(input("Earth's initial y velocity: ")))
Vy.append(float(input("Moon's initial y velocity: ")))

print("Enter the three inital x positions (0, 10, 10.5)")
x.append(float(input("Sun's initial x position: ")))
x.append(float(input("Earth's initial x position: ")))
x.append(float(input("Moon's initial x position: ")))

print("Enter the three inital y positions (0, 0, 0)")
y.append(float(input("Sun's initial y position: ")))
y.append(float(input("Earth's initial y position: ")))
y.append(float(input("Moon's initial y position: ")))

t = 0
dt = 0.0005
maxTime = 10000

filenames, count = [], 0

impactParameter = 0.1
orbitParameter = 3

print("Loading...")

while np.sqrt((x[1] - x[2])**2 + (y[1] - y[2])**2) <= orbitParameter and t < maxTime and np.sqrt((x[0] - x[1])**2 + (y[0] - y[1])**2) > impactParameter and np.sqrt((x[1] - x[2])**2 + (y[1] - y[2])**2) > impactParameter:
    # Compute accelerations at this time
    Ax, Ay = computeAcceleration(masses, x, y)
    
    # Compute new positions and velocities
    x, y, Vx, Vy = eulerStep(x, y, Vx, Vy, Ax, Ay, dt)
    
    # Loop over all possible quarter of a second times
    for i in range(maxTime * 2 + 1):
        # If t is very close to or equal to quarter of a second time: simulate the dynamics
        if abs(t - 0.25 * i) < 0.001:
            fig = plt.figure()
            plt.plot(x[0], y[0], 'y.', x[1], y[1], 'b.', x[2], y[2], 'w.')
            plt.xlim(-12, 12)
            plt.ylim(-12, 12)
            plt.axis('off')
            fig.set_facecolor('k')
            
            filename = f'{count}.png'
            plt.savefig(filename)
            plt.close()
            
            filenames.append(filename)
            
            count += 1
    
    t += dt

if np.sqrt((x[1] - x[2])**2 + (y[1] - y[2])**2) > 3:
    print("Simulation ended: Moon got too far from Earth")
elif np.sqrt((x[0] - x[1])**2 + (y[0] - y[1])**2) <= impactParameter:
    print("Simulation ended: Earth and Sun collided")
elif np.sqrt((x[1] - x[2])**2 + (y[1] - y[2])**2) <= impactParameter:
    print("Simulation ended: Earth and Moon collided")
else:
    print("Simulation ended: Time ran out")

# Build gif
with imageio.get_writer('orbit.gif', mode='I') as writer:
    for filename in filenames:
        writer.append_data(imageio.imread(filename))
        
# Remove files
for filename in set(filenames):
    os.remove(filename)

