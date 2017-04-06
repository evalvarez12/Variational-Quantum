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
    '''
    Psi_T; Padé-Jastrow wave function
    See also: http://www.physics.buffalo.edu/phy411-506/topic5/topic5-lec2.pdf    
    '''
    x1 = np.array(pos[:,0:3])-2
    x2 = np.array(pos[:,3:6])-2
    x12 = np.array(x1-x2)
    r1=np.linalg.norm(x1,axis=1)
    r2=np.linalg.norm(x2,axis=1)
    r12=np.linalg.norm(x12,axis=1)
    
    return np.exp(-2*(r1**2))*np.exp(-2*(r2**2))*np.exp(r12/(2*(1+alpha*(r12))))

def energyLocal(pos, alpha):
    '''
    Local energy of the Padé-Jastrow wave function 
    See also: http://www.physics.buffalo.edu/phy411-506/topic5/topic5-lec2.pdf
    '''
    x1 = np.array(pos[:,0:3])-2
    x2 = np.array(pos[:,3:6])-2
    x12 = np.array(x1-x2)
    r1=np.linalg.norm(x1,axis=1)
    r2=np.linalg.norm(x2,axis=1)
    r12=np.linalg.norm(x12,axis=1)

    f=(1+alpha*r12)    
    
    n12 = (x12/r12[:,None])
    n1 = x1/r1[:,None]
    n2 = x2/r2[:,None]
    d = np.einsum('ij,ij->i', n12 , (n1-n2))
    d /= (f**2)
    
    
    return -4 + alpha/f + alpha/(f**2) + alpha/(f**3) - alpha/(4*(f**4)) + d


def trialDeriv(pos, alpha):    
    ''' d(ln(Psi_T))/d alpha '''
    r=np.linalg.norm(pos,axis=1)
    return -r**2
    

#Simulation parameters
dim=6
iterations = 3000
damping = 5*10**(-8)
startAlpha = 1.8
numTestPoints = 30000
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
