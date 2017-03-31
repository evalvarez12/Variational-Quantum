# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import BoxPlotter
import matplotlib.pyplot as plt
import numpy as np

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




values = [[]]*4
errors = [[]]*4
steps=3
x=(np.array(range(steps))+1)*(2000/steps)
for nt in x:
    print("---------------------")
    print("Number of test points "+str(numTestPoints))    
    
    mcer = MCIntegrator.MCIntegrator(dim=2, numTestPoints=numTestPoints,
                                     domainSize=10, numberOfBoxes=5)
    
    bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)
    
    
    #density=np.random.rand(mcer.numberOfBoxes, mcer.numberOfBoxes)
    density = np.ones([mcer.numberOfBoxes]*mcer.dim)
    
    #np.array([]*4, dtype=np.ndarray)
    for i in range(4):
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
    
        values[i].append(np.average(error))
        errors[i].append(np.std(error))
        print(str(i)+" : "+str(np.average(error[i])) +"±"+ str(np.std(error[i])))

plt.plot(x, np.absolute(errors[0]), '-')
plt.plot(x, np.absolute(errors[1]), '-')
plt.plot(x, np.absolute(errors[2]), '-')
plt.plot(x, np.absolute(errors[3]), '-')
