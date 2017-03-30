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
    return np.exp(-alpha*pos**2)




def energyLocal(pos, alpha):
    return (alpha - alpha**2*2*pos**2 + pos**2/2.)


def trialDeriv(pos, alpha):
    return -pos**2


sim = VQS.VariationalQuantumSimulator(dim=1, numTestPoints=100, domainSize=5, numberOfBoxes=5,
             testFunction=trialWaveFunc, localEnergyFunction=energyLocal, testFuncDeriv=trialDeriv, startAlpha=1., damping=0.8)

energy = []
alphas = []
sim.initializeGrid()
for i in range(10) :
    sim.iterate(True)
    energy += [sim.getEnergy()]
    alphas += [sim.getAlpha()]

# print(energy)
# print(alphas)
