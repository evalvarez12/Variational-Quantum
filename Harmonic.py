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
    return np.exp(-alpha*(np.linalg.norm(pos, axis=1)**2))

def energyLocal(pos, alpha):
    return (alpha - np.linalg.norm(pos, axis=1)**2 * (2* alpha**2 - 1/2))


def trialDeriv(pos, alpha):
    return -np.linalg.norm(pos, axis=1)**2


sim = VQS.VariationalQuantumSimulator(dim=1, numTestPoints=1000, domainSize=2, numberOfBoxes=10,
             testFunction=trialWaveFunc, localEnergyFunction=energyLocal, testFuncDeriv=trialDeriv, startAlpha=1., damping=0.8)

energy = []
alphas = []
#sim.initializeGrid()
for i in range(10) :
    sim.iterate(True)
    print("𝛼: "+ str( sim.getAlpha()))
    print("E: "+ str( sim.getEnergy()))
    energy += [sim.getEnergy()]
    alphas += [sim.getAlpha()]

# print(energy)
# print(alphas)
