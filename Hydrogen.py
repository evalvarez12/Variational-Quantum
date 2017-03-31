# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import BoxPlotter
import VariationalQuantumSimulator as VQS
import matplotlib.pyplot as plt
import numpy as np

RESULT_PATH = "simulation_results"
IMAGE_PATH = RESULT_PATH+"/images"


def trialWaveFunc(pos, alpha):
    r=np.linalg.norm(pos,axis=1)
    return np.exp(-alpha*(r**2))

def energyLocal(pos, alpha):
    r=np.linalg.norm(pos,axis=1)
    return -1/r - 1/2 * alpha * (alpha - 2/r)


def trialDeriv(pos, alpha):    
    r=np.linalg.norm(pos,axis=1)
    return -r**2


sim = VQS.VariationalQuantumSimulator(dim=3, numTestPoints=1000, domainSize=4,
            numberOfBoxes=20, testFunction=trialWaveFunc,
            localEnergyFunction=energyLocal, testFuncDeriv=trialDeriv,
            startAlpha=2, damping=0.0005)

#sim.initializeGrid()

energy = []
alphas = []
for i in range(100):
    sim.iterate(True)
    #sim.alpha=1/2
    print("𝛼: "+ str( sim.getAlpha()))
    print("E: "+ str( sim.getEnergy()))
    energy += [sim.getEnergy()]
    alphas += [sim.getAlpha()]

plt.plot(np.absolute(alphas))
# print(energy)
# print(alphas)
