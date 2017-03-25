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
    
    
    def __init__(self, dim, numTestPoints, domainSize,numberOfBoxes, testFunction):
        self.dim=dim
        self.numTestPoints=numTestPoints
        self.domainSize=domainSize
        self.numberOfBoxes=numberOfBoxes
        self.testFunction=testFunction
        
    def integrate(self):
        f, functionArraySummed = self.testFunction(self.testPointPos, self.dim)
        
        boxIntegral = functionArraySummed*self.testPointVol
        totalIntegral = np.sum(boxIntegral)
        newDensity=np.absolute(boxIntegral)/totalIntegral
        self.iterations+=1
        return np.sum(boxIntegral), boxIntegral, newDensity
            
    def generateAdaptiveStratifiedGrid(self, density, shift=True):
        '''
        Generates a adaptive and stratified grid with ~'numTestPoints'
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
            box = np.random.rand((pointsInBox-directpointsInBox), self.dim)*boxSize
            if shift:
                box += np.array(indicesArr*boxSize)
            
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
        self.testPointPos = boxes
        self.testPointVol = volumes
        
    def generateStratifiedGrid(self):
        '''
        Generates uniform grid with ~'numTestPoints'
        '''
        density=np.ones([self.numberOfBoxes]*self.dim)
        self.generateAdaptiveStratifiedGrid(density=density)
        
    def generateUniformGrid(self):
        '''
        Generates uniform grid with ~'numTestPoints'
        '''
        density=np.ones([self.numberOfBoxes]*self.dim)
        self.generateAdaptiveStratifiedGrid(density=density, shift=False)
        
    def generateAdaptiveUniformGrid(self, density):
        '''
        Generates uniform adaptive grid with ~'numTestPoints'
        according to the density distribution 'density'
        '''
        self.generateAdaptiveStratifiedGrid(density=density, shift=False)
        
    def getFlatTestPoints(self):
        d=self.dim
        a=self.testPointPos
        while d>0:
            a=np.concatenate(a, axis=0)
            d-=1
        return a
        
    def getEnergy(self):
        return self.energy