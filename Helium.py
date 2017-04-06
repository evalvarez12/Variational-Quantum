# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene


Find the best alpha-parameter for the test-wave-function for Hydrogen.
We are using the test-function given in Chapter 12 of the book
"Computational Physics" by JM Thijssen. All equation numberings refer to this book.
"""

import BoxPlotter
import VariationalQuantumSimulator as VQS
import matplotlib.pyplot as plt
import numpy as np
import csv


def trialWaveFunc(pos, alpha):
    ''' Psi_T; page 377 '''
    r=np.linalg.norm(pos,axis=1)
    return np.exp(-alpha*(r**2))

def energyLocal(pos, alpha):
    ''' E_L; equation 12.10 '''
    r=np.linalg.norm(pos,axis=1)
    return -1/r - 1/2 * alpha * (alpha - 2/r)


def trialDeriv(pos, alpha):    
    ''' d(ln(Psi_T))/d alpha '''
    r=np.linalg.norm(pos,axis=1)
    return -r**2
    

#Simulation parameters
iterations = 100
damping = 0.00005
startAlpha = 3
numTestPoints = 5000
domainSize = 4
numberOfBoxes = 7

RESULT_PATH = "results/systems"
IMAGE_PATH = RESULT_PATH+"/images"


#Create a CSV-Logger for the results
CSV_FILE = open(RESULT_PATH+"/hydrogen-log_it-"+str(iterations)+"_damp-"+str(damping)+"_nTP-"+str(numTestPoints)+"_-sA"+str(startAlpha)+".csv", 'w', newline='')
dic = ['iterations', 'energy', 'alpha', 'corr', 'corrA']
CSV_FILE_WRITER = csv.DictWriter(CSV_FILE, dic)


sim = VQS.VariationalQuantumSimulator(dim=3, numTestPoints=numTestPoints, domainSize=domainSize,
            numberOfBoxes=numberOfBoxes, testFunction=trialWaveFunc,
            localEnergyFunction=energyLocal, testFuncDeriv=trialDeriv,
            startAlpha=startAlpha, damping=damping)

#sim.initializeGrid()

energy = []
alphas = []
for i in range(iterations):
    print("𝛼: "+ str( sim.getAlpha()))
    alphas += [sim.getAlpha()]
    sim.iterate(True)
    energy += [sim.getEnergy()]
    print("E: "+ str( sim.getEnergy()))
    print("dE/d𝛼: "+ str( sim.getCorrection()))
    print("𝛾 dE/d𝛼: "+ str( sim.getAlphaCorrection()))
    CSV_FILE_WRITER.writerow({'iterations' : i, 'energy' : energy[i], 'alpha' : alphas[i], 'corr' : sim.getCorrection(), 'corrA' : sim.getCorrection()})

CSV_FILE.flush()
CSV_FILE.close()

CSV_FILE = open(RESULT_PATH+"/hydrogen-wf_it-"+str(iterations)+"_damp-"+str(damping)+"_nTP-"+str(numTestPoints)+"_-sA"+str(startAlpha)+".csv", 'w', newline='')
CSV_FILE_WRITER = csv.writer(CSV_FILE)

wfden, pos = sim.getWFDensity()

for i in range(len(pos)):
    CSV_FILE_WRITER.writerow([*tuple(pos[i]), wfden[i]])


plt.plot(np.absolute(alphas))
