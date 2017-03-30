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


sim = VQS.VariationalQuantumSimulator(dim=1, numTestPoints=2000, domainSize=4,
            numberOfBoxes=20, testFunction=trialWaveFunc,
            localEnergyFunction=energyLocal, testFuncDeriv=trialDeriv,
            startAlpha=0.6, damping=0.8)

energy = []
alphas = []
#sim.initializeGrid()
for i in range(10) :
    sim.iterate(False)
    sim.alpha=1/2
    print("𝛼: "+ str( sim.getAlpha()))
    print("E: "+ str( sim.getEnergy()))
    energy += [sim.getEnergy()]
    alphas += [sim.getAlpha()]

# print(energy)
# print(alphas)
