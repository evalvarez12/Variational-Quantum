# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import BoxPlotter
import matplotlib.pyplot as plt
import numpy as np
import csv

RESULT_PATH = "simulation_results"
IMAGE_PATH = RESULT_PATH+"/images"


iterations = 500
#analyticalAnswer = 1666.666666666   # (2nd line)
#analyticalAnswer = 7.24378          # (4th line)
#analyticalAnswer = 23.04            # (Heaviside if-statement)
analyticalAnswer = 2*np.pi*(3**2-2**2)



def hyperbel(pos):
    return np.sum((pos[:]-5.)**2., axis=1)

def ringStep(pos):
    d = np.linalg.norm(pos-5, axis=1)
    return ((d>2) & (d<3))*2




steps=100
values = np.zeros([4,steps])
errors = np.zeros([4,steps])
x=(np.array(range(steps))+1)*int(4000/steps)

for i in range(4):
    CSV_FILE = open("integration_ringStep_it-"+str(iterations)+"_step-"+str(steps)+"_met-"+str(i)+".csv", 'w', newline='')  
    CSV_FILE_WRITER = csv.writer(CSV_FILE)
    
    for run in range(steps):
        numTestPoints = x[run]
        print("---------------------")
        print("Number of test points: " + str(numTestPoints))
        print("Grid method: " + str(i))
        print("Number of Test points: " + str(numTestPoints))
        
        mcer = MCIntegrator.MCIntegrator(dim=2, numTestPoints=numTestPoints,
                                         domainSize=10, numberOfBoxes=5)
        
        #bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)
        
        
        density = np.ones([mcer.numberOfBoxes]*mcer.dim)
        
        
        error = []
        for itera in range(iterations):
            if i == 0:
                mcer.generateUniformGrid()
            elif i == 1:
                mcer.generateAdaptiveUniformGrid(density=density)
            elif i == 2:
                mcer.generateStratifiedGrid()
            elif i == 3:
                mcer.generateAdaptiveStratifiedGrid(density=density)
    
            totalIntegral, boxIntegral, newDensity = mcer.integrate(function=ringStep)
            error = np.append(error,[abs(1-(totalIntegral/analyticalAnswer))])
    
            #print(totalIntegral)
            #bplotter.plotBox(True, False)
    
            density = newDensity
    
        values[i, run] = (np.average(error))
        errors[i, run] = (np.std(error))
        CSV_FILE_WRITER.writerow([numTestPoints, values[i, run], errors[i, run]])
        print(" > "+str(np.average(error)) +"±"+ str(np.std(error)))
        
    CSV_FILE.flush()
    CSV_FILE.close()

plt.plot(x, np.absolute(values[0]), '-o')
plt.plot(x, np.absolute(values[1]), '-o')
plt.plot(x, np.absolute(values[2]), '-o')
plt.plot(x, np.absolute(values[3]), '-o')
