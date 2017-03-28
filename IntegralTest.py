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


iterations = 1000
#analyticalAnswer = 1666.666666666   # (2nd line)
#analyticalAnswer = 7.24378          # (4th line)
#analyticalAnswer = 23.04            # (Heaviside if-statement)
analyticalAnswer = 2*np.pi*(3**2-2**2)



def funcWrapper(func, pos, dim):
    numberOfBoxes = len(pos)
    f = np.array(np.zeros([numberOfBoxes]*dim), dtype=np.ndarray)
    f_sum = np.array(np.zeros([numberOfBoxes]*dim), dtype=float)

    boxesindices = np.array(np.meshgrid(*[range(numberOfBoxes)]*dim)).T.reshape(-1, dim)
    for indices in boxesindices:
        indices = tuple(indices)
        f[indices] = func(np.array(pos[indices]))
        f_sum[indices] = sum(f[indices])

    return f, f_sum

def hyperbel(pos):
    return np.sum((pos[:]-5.)**2., axis=1)

def ringStep(pos):
    d = np.linalg.norm(pos-5, axis=1)
    return ((d>2) & (d<3))*2


def testFunction(pos, dim):
    return funcWrapper(ringStep, pos, dim)

mcer = MCIntegrator.MCIntegrator(dim=2, numTestPoints=2000, domainSize=10, numberOfBoxes=5, testFunction=testFunction)

bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)


#density=np.random.rand(mcer.numberOfBoxes, mcer.numberOfBoxes)
density = np.ones([mcer.numberOfBoxes]*mcer.dim)

#np.array([]*4, dtype=np.ndarray)
errors = [[]]*4
for i in range(4):
    for itera in range(iterations):
        if i == 0:
            mcer.generateUniformGrid()
        elif i == 1:
            mcer.generateAdaptiveUniformGrid(density=density)
        elif i == 2:
            mcer.generateStratifiedGrid()
        elif i == 3:
            mcer.generateAdaptiveStratifiedGrid(density=density)

        totalIntegral, boxIntegral, newDensity = mcer.integrate()
        errors[i] = np.append(errors[i],[abs(1-(totalIntegral/analyticalAnswer))])

        #print(totalIntegral)
        #bplotter.plotBox(True, False)

        density = newDensity

    print(str(np.average(errors[i])) +"±"+ str(np.std(errors[i])))
#plt.plot(np.absolute(error))
