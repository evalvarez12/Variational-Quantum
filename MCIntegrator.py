# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:25:01 2017

@author: rene
"""

import numpy as np


class MCIntegrator:
    dim = 2
    numberOfBoxes = 5
    testPointVol = []
    testPointPos = []
    domainSize=10
    
    def __init__(self):
        #density=np.random.rand(numberOfBoxesPerDimension, numberOfBoxesPerDimension)#np.ones([x,y])
        density=np.ones([self.numberOfBoxes, self.numberOfBoxes])
        density /= np.sum(density)
        self.generateGrid(density=density, numberTestPoints=1000)
    
    def generateGrid(self, density, numberTestPoints):
        '''
        Generates a adaptivem stratified grid with ~'numberTestPoints'
        according to the density distribution 'density'
        '''
        density /= np.sum(density)
        
        boxSize = self.domainSize/self.numberOfBoxes
        
        boxes = np.array([[0]*self.numberOfBoxes]*self.numberOfBoxes, dtype=np.ndarray)
        volumes = np.array([[0]*self.numberOfBoxes]*self.numberOfBoxes, dtype=float)
        numberTestPoints = density*numberTestPoints
        numberTestPoints = numberTestPoints.astype(int)
        
        for i in range(len(boxes)):
            for j in range(len(boxes[:])):
                pointsInBox = int(round(density[i,j]*numberTestPoints))
                pointsPerDirection = int(pointsInBox**(1/self.dim))
                directpointsInBox = int(pointsPerDirection**self.dim)
        
                box = np.random.rand((pointsInBox-directpointsInBox), self.dim)*boxSize+np.array([(i*boxSize), (j*boxSize)])
                
                if pointsPerDirection > 0:
                    l = boxSize/pointsPerDirection
                    
                    a=np.linspace((i*boxSize), ((i+1)*boxSize), pointsPerDirection, endpoint=False)
                    b=np.linspace((j*boxSize), ((j+1)*boxSize), pointsPerDirection, endpoint=False)
                    box1 = np.transpose([np.tile(a, len(b)), np.repeat(b, len(a))])
                    box1 += np.random.rand(directpointsInBox, self.dim)*l
                    box = np.concatenate([box1, box])
                boxes[i,j] = box
                volumes[i,j] = (boxSize**self.dim)/pointsInBox
                
        boxes = np.array(boxes)
        volumes = np.array(volumes)
        self.testPointPos = boxes #np.concatenate(np.concatenate(boxes, axis=0), axis=0)
        self.testPointVol = volumes #np.concatenate(np.concatenate(volumes, axis=0), axis=0)