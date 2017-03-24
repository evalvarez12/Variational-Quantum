# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:25:01 2017

@author: rene
"""

import numpy as np


class MCIntegrator:
    dim = 3
    numberOfBoxes = 2
    testPointVol = []
    testPointPos = []
    domainSize=1
    numTestPoints = 8
    iterations=0
    energy=0
    
    
    def __init__(self, dim, numTestPoints, domainSize,numberOfBoxes):
        self.dim=dim
        self.numTestPoints=numTestPoints
        self.domainSize=domainSize
        self.numberOfBoxes=numberOfBoxes
        density=np.random.rand(*[self.numberOfBoxes]*self.dim)#np.ones([x,y])
        #density=np.ones([self.numberOfBoxes, self.numberOfBoxes])
        density /= np.sum(density)
        self.generateGrid(density=density)
        
    def applyFunction(self, pos):
        #return np.sum((pos[:]-5)**2, axis=1)
    
        f = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=np.ndarray)
        f_sum = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=float)
    
    
        boxesindices = np.array(np.meshgrid(*[range(self.numberOfBoxes)]*self.dim)).T.reshape(-1,self.dim)
        for indices in boxesindices:
            indices=tuple(indices)
            f[indices] = (pos[indices][:,0]-5)**2 + (pos[indices][:,1]-5)**2
            f_sum[indices] = sum(f[indices]) 
    
        return f, f_sum
    
    def integrate(self):
        f, f_sum = self.applyFunction(self.testPointPos)
        box_int = f_sum*self.testPointVol
    
        return np.sum(box_int), box_int
            


    
    def generateGrid(self, density):
        '''
        Generates a adaptivem stratified grid with ~'numTestPoints'
        according to the density distribution 'density'
        '''
        density /= np.sum(density)
        
        boxSize = self.domainSize/self.numberOfBoxes
        
        boxes = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=np.ndarray)
        volumes = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=float)
        #numTestPoints = density*numTestPoints
        #numTestPoints = numTestPoints.astype(int)
        boxesindices = np.array(np.meshgrid(*[range(self.numberOfBoxes)]*self.dim)).T.reshape(-1,self.dim)
        for indices in boxesindices:
            indicesArr=indices
            indices=tuple(indices)
            pointsInBox = max(1,int(round(density[indices]*self.numTestPoints)))
            pointsPerDirection = int(pointsInBox**(1/self.dim))
            directpointsInBox = int(pointsPerDirection**self.dim)
    
            #Generate the random points, that don't fit in the grid
            box = np.random.rand((pointsInBox-directpointsInBox), self.dim)*boxSize + np.array(indicesArr*boxSize)
            
            #Generate the stratified grid-points
            if pointsPerDirection > 0:
                #Generate the even grid
                linspaces=[np.linspace((i*boxSize), ((i+1)*boxSize), pointsPerDirection, endpoint=False) for i in indices]
                box1 = np.array(np.meshgrid(*linspaces)).T.reshape(-1,self.dim)
                #Now move (stratify) the grid-points
                l = boxSize/pointsPerDirection
                box1 += np.random.rand(directpointsInBox, self.dim)*l
                box = np.concatenate([box1, box])
            boxes[indices] = box
            volumes[indices] = (boxSize**self.dim)/pointsInBox
                
        boxes = np.array(boxes)
        volumes = np.array(volumes)
        self.testPointPos = boxes #np.concatenate(np.concatenate(boxes, axis=0), axis=0)
        self.testPointVol = volumes #np.concatenate(np.concatenate(volumes, axis=0), axis=0)
        
    def getFlatTestPoints(self):
        d=self.dim
        a=self.testPointPos
        while d>0:
            a=np.concatenate(a, axis=0)
            d-=1
        return a
        
    def getEnergy(self):
        return self.energy