# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import BoxPlotter
import VariationalQuantumSimulator as VQS
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

RESULT_PATH = "simulation_results"
IMAGE_PATH = RESULT_PATH+"/images"


def trialWaveFunc(pos, alpha):
    return np.exp(-alpha*(pos[:,0]**2))

def energyLocal(pos, alpha):
    return (alpha - pos[:,0]**2 * (2* alpha**2 - 1/2))


def trialDeriv(pos, alpha):
    return -pos[:,0]**2


sim = VQS.VariationalQuantumSimulator(dim=1, numTestPoints=1000, domainSize=4,
            numberOfBoxes=20, testFunction=trialWaveFunc,
            localEnergyFunction=energyLocal, testFuncDeriv=trialDeriv,
            startAlpha=1, damping=0.0005)

#sim.initializeGrid()

energy = []
alphas = []
for i in range(100) :
    print("𝛼: "+ str( sim.getAlpha()))
    alphas += [sim.getAlpha()]
    sim.iterate(True)
    energy += [sim.getEnergy()]
    print("E: "+ str( sim.getEnergy()))

plt.plot(np.absolute(alphas))
# print(energy)
# print(alphas)
