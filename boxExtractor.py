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
steps = 100
iterations = 5
numberOfBoxes = 5

#ringStep
intFunc = ringStep
analyticalAnswer = 2*np.pi*(3**2-2**2)
domainSize = 10
dim = 2

numTestPoints = 25*(3**2)

#hyperbel
#intFunc = hyperbel
#analyticalAnswer = 1/6
#domainSize = 1
#dim=2

RESULT_PATH = "results/integration_test"
IMAGE_PATH = RESULT_PATH+"/images"


#For each of the four integration methods
for i in range(4):
    
    
    print("---------------------")
    print("Grid method: " + str(i))
    print("Number of Test points: " + str(numTestPoints))
    
    mcer = MCIntegrator.MCIntegrator(dim=dim, numTestPoints=numTestPoints,
        domainSize=domainSize, numberOfBoxes=numberOfBoxes)
    
    bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)
    
    density = np.ones([mcer.numberOfBoxes]*mcer.dim)
    
    #Run the number of iterations specified
    for itera in range(iterations):
        if i == 0:
            mcer.generateUniformGrid()
        elif i == 1:
            mcer.generateAdaptiveUniformGrid(density=density)
        elif i == 2:
            mcer.generateStratifiedGrid()
        elif i == 3:
            mcer.generateAdaptiveStratifiedGrid(density=density)

        totalIntegral, _, newDensity = mcer.integrate(function=intFunc)

        #print(totalIntegral)

        density = newDensity
        
    bplotter.plotBox(True, True)
    CSV_FILE = open(RESULT_PATH+"/ringStep_mesh_N-"+str(numTestPoints)+"_met-"+str(i)+".csv", 'w', newline='')  
    CSV_FILE_WRITER = csv.writer(CSV_FILE)
    points=mcer.getFlatTestPoints()
    for p in points:
        CSV_FILE_WRITER.writerow(p)
        CSV_FILE.flush()
    CSV_FILE.close()

