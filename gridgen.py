# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:35:40 2017

@author: rene
"""

2# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import time
import numpy as np
#import scipy
from scipy.stats import maxwell
#import xlwt


totalNumberOfParticles=40
x,y=2,2
boxes = [[[]]*x]*y
density = np.random.rand(x,y)
density /= np.sum(density)
boxSize = 5
dim=2

for i in range(len(boxes)):
    for j in range(len(boxes[:])):
        print("generate box "+str(i)+":"+str(j))
        particlesInBox = int(density[i,j]*totalNumberOfParticles)
        particlesPerDirection = int(particlesInBox**(1/dim))
        directParticlesInBox = particlesPerDirection**dim
        
        boxes[i][j] = [[0]*dim]*directParticlesInBox
        a=np.linspace((i*boxSize), ((i+1)*boxSize), particlesPerDirection)
        print(a)
        b=np.linspace((j*boxSize), ((j+1)*boxSize), particlesPerDirection)
        print(b)
        box = np.transpose([np.tile(a, len(b)), np.repeat(b, len(a))])
        print(box)
        boxes[i][j] = box
        
        

