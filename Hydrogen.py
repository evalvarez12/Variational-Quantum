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
analyticalAnswer = 1



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

def hydrogenTestFunction(pos):
    return np.sum((pos[:]-5)**2, axis=1)


def testFunction(pos, dim):
    return funcWrapper(hydrogenTestFunction, pos, dim)

mcer = MCIntegrator.MCIntegrator(dim=2, numTestPoints=70, domainSize=10, numberOfBoxes=5, testFunction=testFunction)

bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)


#density=np.random.rand(mcer.numberOfBoxes, mcer.numberOfBoxes)
density = np.ones([mcer.numberOfBoxes]*mcer.dim)

error=[]
for i in range(0,iterations):
    mcer.generateGrid(density=density)
    totalIntegral, boxIntegral, newDensity = mcer.integrate()
    error = np.append(error,[abs(1-(totalIntegral/analyticalAnswer))])

    print(totalIntegral)
    #bplotter.plotBox(True, False)

    density = newDensity


print(str(np.average(error)) + "±" + str(np.std(error)))
plt.plot(np.absolute(error))
