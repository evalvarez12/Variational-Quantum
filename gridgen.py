# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:35:40 2017

@author: rene
"""
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import time
import numpy as np
#import scipy
from scipy.stats import maxwell
#import xlwt
import matplotlib.pyplot as plt


def f(pos):
    return np.sum((pos[:]-5)**2, axis=1)
    
def integral():
    f(boxes)

totalNumberOfParticles = 1000
numberOfBoxesPerDimension = 5
boxes = np.array([[0]*numberOfBoxesPerDimension]*numberOfBoxesPerDimension, dtype=np.ndarray)
volumes = np.array([[0]*numberOfBoxesPerDimension]*numberOfBoxesPerDimension, dtype=float)
density = np.ones([numberOfBoxesPerDimension,numberOfBoxesPerDimension])#np.random.rand(numberOfBoxesPerDimension, numberOfBoxesPerDimension)#np.ones([x,y])#
density /= np.sum(density)
numberOfParticles = density*totalNumberOfParticles
numberOfParticles = numberOfParticles.astype(int)

boxSize = 1/numberOfBoxesPerDimension
dim=2

for i in range(len(boxes)):
    for j in range(len(boxes[:])):        
        particlesInBox = int(round(density[i,j]*totalNumberOfParticles))
        particlesPerDirection = int(particlesInBox**(1/dim))
        directParticlesInBox = int(particlesPerDirection**dim)

        box = np.random.rand((particlesInBox-directParticlesInBox), dim)*boxSize+np.array([(i*boxSize), (j*boxSize)])
        
        if particlesPerDirection > 0:
            l = boxSize/particlesPerDirection
            
            #boxes[i][j] = [[0]*dim]*directParticlesInBox
            a=np.linspace((i*boxSize), ((i+1)*boxSize), particlesPerDirection, endpoint=False)
            b=np.linspace((j*boxSize), ((j+1)*boxSize), particlesPerDirection, endpoint=False)
            box1 = np.transpose([np.tile(a, len(b)), np.repeat(b, len(a))])
            box1 += np.random.rand(directParticlesInBox, dim)*l
            box = np.concatenate([box1, box])
        boxes[i,j] = box
        volumes[i,j] = boxSize**dim/particlesInBox
        
boxes = np.array(boxes)
arr = np.concatenate(np.concatenate(boxes, axis=0), axis=0)

plt.rcParams["figure.figsize"] = [8,8]
plt.figure()
        
ax = plt.gca()
ax.set_xlim([0,1])
ax.set_ylim([0,1])


#plt.plot(arr, 'ro')
plt.plot(arr[:,0],arr[:,1], 'r.')


plt.draw()
#plt.savefig(SAVE_PATH+"/"+str(simNum)+"-"+key+".png", box_inches='tight', dpi=100)
plt.show()
plt.close()
        
        

