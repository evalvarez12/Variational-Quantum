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
    numTestPoints = 1000
    iterations=0
    energy=0
    
    
    
    def __init__(self):
        density=np.random.rand(self.numberOfBoxes, self.numberOfBoxes)#np.ones([x,y])
        #density=np.ones([self.numberOfBoxes, self.numberOfBoxes])
        density /= np.sum(density)
        self.generateGrid(density=density)
        
    def applyFunction(self, pos):
        #return np.sum((pos[:]-5)**2, axis=1)
    
        f = np.array([[0]*self.numberOfBoxes]*self.numberOfBoxes, dtype=np.ndarray)
        f_sum = np.array([[0]*self.numberOfBoxes]*self.numberOfBoxes)
    
        for i in range(len(self.testPointPos)):
            for j in range(len(self.testPointPos[:])): 
                f[i][j] = (pos[i][j][:,0]-5)**2 + (pos[i][j][:,1]-5)**2
                f_sum[i][j] = sum(f[i][j]) 
    
        return f, f_sum
    
    def integrate(self):
        f, f_sum = self.applyFunction(self.testPointPos)
        box_int = f_sum*self.testPointVol
        
        print(np.sum(box_int))
    
        return np.sum(box_int), box_int
            


    
    def generateGrid(self, density):
        '''
        Generates a adaptivem stratified grid with ~'numTestPoints'
        according to the density distribution 'density'
        '''
        density /= np.sum(density)
        
        boxSize = self.domainSize/self.numberOfBoxes
        
        boxes = np.array([[0]*self.numberOfBoxes]*self.numberOfBoxes, dtype=np.ndarray)
        volumes = np.array([[0]*self.numberOfBoxes]*self.numberOfBoxes, dtype=float)
        #numTestPoints = density*numTestPoints
        #numTestPoints = numTestPoints.astype(int)
        
        for i in range(len(boxes)):
            for j in range(len(boxes[:])):
                pointsInBox = int(round(density[i,j]*self.numTestPoints))
                pointsPerDirection = int(pointsInBox**(1/self.dim))
                directpointsInBox = int(pointsPerDirection**self.dim)
        
                #Generate the random points, that don't fit in the grid
                box = np.random.rand((pointsInBox-directpointsInBox), self.dim)*boxSize+np.array([(i*boxSize), (j*boxSize)])
                
                #Generate the stratified grid-points
                if pointsPerDirection > 0:
                    #Generate the even grid
                    a=np.linspace((i*boxSize), ((i+1)*boxSize), pointsPerDirection, endpoint=False)
                    b=np.linspace((j*boxSize), ((j+1)*boxSize), pointsPerDirection, endpoint=False)
                    box1 = np.transpose([np.tile(a, len(b)), np.repeat(b, len(a))])
                    #Now move (stratify) the grid-points
                    l = boxSize/pointsPerDirection
                    box1 += np.random.rand(directpointsInBox, self.dim)*l
                    box = np.concatenate([box1, box])
                boxes[i,j] = box
                volumes[i,j] = (boxSize**self.dim)/pointsInBox
                
        boxes = np.array(boxes)
        volumes = np.array(volumes)
        self.testPointPos = boxes #np.concatenate(np.concatenate(boxes, axis=0), axis=0)
        self.testPointVol = volumes #np.concatenate(np.concatenate(volumes, axis=0), axis=0)
        
    def getFlatTestPoints(self):
        return np.concatenate(np.concatenate(self.testPointPos, axis=0), axis=0)
        
    def getEnergy(self):
        return self.energy