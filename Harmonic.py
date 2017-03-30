# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import BoxPlotter
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

RESULT_PATH = "simulation_results"
IMAGE_PATH = RESULT_PATH+"/images"


iterations = 1000
analyticalAnswer = .5





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


def expectedValH(x, a):
    e = normalizationFactor(x, a)
    energyLoc = energyLocal(x, a)
    return e*energyLoc


def normalizationFactor(x, a):
    return np.exp(-2*a*x**2)


def energy(x, a):
    energy = expectedValH(x, a)/normalizationFactor(x, a)
    return energy


def energyLocal(x, a):
    return (1/2.)*(a - a**2*4*x**2 + x**2)


def testFunction(func, pos, dim):
    return funcWrapper(func, pos, dim)


def dE(x, a):


def minimizer()




#density=np.random.rand(mcer.numberOfBoxes, mcer.numberOfBoxes)


mcerNormalization = MCIntegrator.MCIntegrator(dim=2, numTestPoints=1000, domainSize=10, numberOfBoxes=5, testFunction=intNormalization)
mcerExpectedValH = MCIntegrator.MCIntegrator(dim=2, numTestPoints=1000, domainSize=10, numberOfBoxes=5, testFunction=intExpectedValH)
mcerX2 = MCIntegrator.MCIntegrator(dim=2, numTestPoints=1000, domainSize=10, numberOfBoxes=5, testFunction=intX2)
mcerELocalX2 = MCIntegrator.MCIntegrator(dim=2, numTestPoints=1000, domainSize=10, numberOfBoxes=5, testFunction=intELocalX2)
bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)


error=[]

a = 1.
for i in range(iterations):

    densityNormalization = np.ones([mcer.numberOfBoxes]*mcer.dim)
    densityExpectedValH = np.ones([mcer.numberOfBoxes]*mcer.dim)
    densityX2 = np.ones([mcer.numberOfBoxes]*mcer.dim)
    densityELocalX2 = np.ones([mcer.numberOfBoxes]*mcer.dim)

    for j in range(5) :
        mcerNormalization.generateAdaptiveStratifiedGrid(density=Normalizationdensity)
        mcerExpectedValH.generateAdaptiveStratifiedGrid(density=ExpectedValHdensity)
        mcerX2.generateAdaptiveStratifiedGrid(density=X2density)
        mcerELocalX2.generateAdaptiveStratifiedGrid(density=ELocalX2density)

        totalIntegralNormalization, boxIntegralNormalization, densityNormalization = mcerNormalization.integrate()
        totalIntegralExpectedValH, boxIntegralExpectedValH, densityExpectedValH = mcerExpectedValH.integrate()
        totalIntegralX2, boxIntegralX2, densityX2 = mcerX2.integrate()
        totalIntegralELocalX2, boxIntegralELocalX2, densityELocalX2 = mcerELocalX2.integrate()

    # totalIntegral, boxIntegral, newDensity = mcer.integrate()
    error = np.append(error, [abs(1-(totalIntegral/analyticalAnswer))])
    print(totalIntegral)
    # bplotter.plotBox(True, False)



# print(str(np.average(error)) + "±" + str(np.std(error)))
# plt.plot(np.absolute(error))
