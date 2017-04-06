# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene

Benchmarks the performance of different numerical Integration methods.
"""

import MCIntegrator
import BoxPlotter
import matplotlib.pyplot as plt
import numpy as np
import csv
import time




def hyperbel(pos):
    '''
    analyticalAnswer = 1/6
    domain = 1
    dim = 2
    '''
    return np.sum((pos[:]-5.)**2., axis=1)

def ringStep(pos):
    '''
    Doghnut-shaped area with value 2;
    analyticalAnswer = 2*np.pi*(3**2-2**2)
    domain >= 6
    dim = 2
    '''
    d = np.linalg.norm(pos-5, axis=1)
    return ((d>2) & (d<3))*2




#Simulation parameters
steps = 250
iterations = 1000
numberOfBoxes = 5
maxNumPoints = 3000
minNumPoints = 100

#ringStep
intFunc = ringStep
analyticalAnswer = 2*np.pi*(3**2-2**2)
domainSize = 10
dim = 2
addRandom=True

#hyperbel
#intFunc = hyperbel
#analyticalAnswer = 1/6
#domainSize = 1
#dim=2

RESULT_PATH = "results/integration_test"
IMAGE_PATH = RESULT_PATH+"/images"



#Local iteration storage
values = np.zeros([4,steps])
errors = np.zeros([4,steps])
rx = np.zeros([4,steps])
x=(np.array(range(steps)))*int((maxNumPoints-minNumPoints)/steps+minNumPoints)


#For each of the four integration methods
for i in range(4):
    #Create a CSV-Logger for the results
    CSV_FILE = open(RESULT_PATH+"/ringStep"+"_r-"+str(addRandom)+"_it-"+str(iterations)+"_step-"+str(steps)+"_maxN-"+str(maxNumPoints)+"_met-"+str(i)+".csv", 'w', newline='')  
    CSV_FILE_WRITER = csv.writer(CSV_FILE)
    
    #Run for different number of points
    for run in range(steps):
        startTime = time.time()
        
        realTP=[]
        numTestPoints = x[run]
        print("---------------------")
        print("Grid method: " + str(i))
        print("Number of Test points: " + str(numTestPoints))
        
        mcer = MCIntegrator.MCIntegrator(dim=dim, numTestPoints=numTestPoints,
            domainSize=domainSize, numberOfBoxes=numberOfBoxes)
        
        #bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)
        
        density = np.ones([mcer.numberOfBoxes]*mcer.dim)
        
        
        error = []
        
        #Run the number of iterations specified
        for itera in range(iterations):
            if i == 0:
                mcer.generateUniformGrid(addRandom=addRandom)
            elif i == 1:
                mcer.generateAdaptiveUniformGrid(density=density, addRandom=addRandom)
            elif i == 2:
                mcer.generateStratifiedGrid(addRandom=addRandom)
            elif i == 3:
                mcer.generateAdaptiveStratifiedGrid(density=density, addRandom=addRandom)
    
            realTP += [mcer.actNumberOfTestPoints]
            totalIntegral, _, newDensity = mcer.integrate(function=intFunc)
            error = np.append(error,[abs(1-(totalIntegral/analyticalAnswer))])
    
            #print(totalIntegral)
            #bplotter.plotBox(True, False)
    
            density = newDensity
    
        values[i, run] = (np.average(error))
        errors[i, run] = (np.std(error))
        realTestPoints = np.average(realTP)
        rx[i, run] =  realTestPoints
        realTestPointsErr = np.std(realTP)
        t = time.time() - startTime
        
        #Write the changes to the CSV and console
        CSV_FILE_WRITER.writerow([realTestPoints, values[i, run], errors[i, run], realTestPointsErr, t, numTestPoints])
        CSV_FILE.flush()
        
        print(" > Actual number of points was "+str(realTestPoints))
        print(" > The error was on avarage "+str(np.average(error)) +"±"+ str(np.std(error)))
        print(" > It took "+str(t)+"s")
    CSV_FILE.close()

plt.plot(rx[0], np.absolute(values[0]), '-o')
plt.plot(rx[1], np.absolute(values[1]), '-o')
plt.plot(rx[2], np.absolute(values[2]), '-o')
plt.plot(rx[3], np.absolute(values[3]), '-o')
