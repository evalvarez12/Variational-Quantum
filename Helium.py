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
    r1=np.linalg.norm(pos[:,0:2],axis=1)
    r2=np.linalg.norm(pos[:,3:5],axis=1)
    r12=np.linalg.norm(pos[:,3:5]-pos[:,0:2],axis=1)
    return np.exp(-alpha*(r1**2))*np.exp(-alpha*(r2**2))*np.exp(r12/(2*(1+alpha*(r12))))

def energyLocal(pos, alpha):
    ''' E_L; equation 12.10 '''
    print(len(pos))
    print(len(pos[0]))
    x1=pos[:,0:2]
    x2=pos[:,3:5]
    x12 = x2-x1
    r1=np.linalg.norm(x1,axis=1)
    r2=np.linalg.norm(x2,axis=1)
    r12=np.linalg.norm(x12,axis=1)
    print(x1)
    print(x2)
    return -4 + alpha/(1+alpha*r12) + alpha/((1+alpha*r12)**2) + alpha/((1+alpha*r12)**3) - alpha/(4*(1+alpha*r12)**4) + ((x12/r12)*(x1/r1-x2/r2))/(1+alpha*r12)


def trialDeriv(pos, alpha):    
    ''' d(ln(Psi_T))/d alpha '''
    r=np.linalg.norm(pos,axis=1)
    return -r**2
    

#Simulation parameters
dim=6
iterations = 100
damping = 0.00005
startAlpha = 3
numTestPoints = 5000
domainSize = 4
numberOfBoxes = 3

RESULT_PATH = "results/systems"
IMAGE_PATH = RESULT_PATH+"/images"


#Create a CSV-Logger for the results
CSV_FILE = open(RESULT_PATH+"/hydrogen-log_it-"+str(iterations)+"_damp-"+str(damping)+"_nTP-"+str(numTestPoints)+"_-sA"+str(startAlpha)+".csv", 'w', newline='')
dic = ['iterations', 'energy', 'alpha', 'corr', 'corrA']
CSV_FILE_WRITER = csv.DictWriter(CSV_FILE, dic)


sim = VQS.VariationalQuantumSimulator(dim=dim, numTestPoints=numTestPoints, domainSize=domainSize,
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
