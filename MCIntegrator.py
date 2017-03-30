# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:25:01 2017

@author: rene
"""

import numpy as np


class MCIntegrator:
    '''
    This class allows you to perform numerical integrations on functions.
    It works in all dimensionalities.
    You can use different methods of generating a grid of random points.
    Available are stratified and uniform grid with or without adaptiveness.
    '''

    #Dimensionality of the problem
    dim = 3
    #Number of integration evaluation points
    numTestPoints = 2000
    #Size of the integration domain
    domainSize = 4
    #Number of boxes per dimension for adaptiveness
    numberOfBoxes = 50

    #Local variables. Don't change
    testPointVol = []
    testPointPos = []


    def __init__(self, dim, numTestPoints, domainSize, numberOfBoxes):
        self.dim=dim
        self.numTestPoints=numTestPoints
        self.domainSize=domainSize
        self.numberOfBoxes=numberOfBoxes

    def integrate(self, function):
        f, functionArraySummed = function(self.testPointPos)

        boxIntegral = functionArraySummed*self.testPointVol
        totalIntegral = np.sum(boxIntegral)
        newDensity = np.absolute(boxIntegral)/totalIntegral
        return np.sum(boxIntegral), boxIntegral, newDensity

    def generateAdaptiveStratifiedGrid(self, density, shift=True):
        '''
        Generates a adaptive and stratified grid with ~'numTestPoints'
        according to the density distribution 'density'
        '''
        density /= np.sum(density)
        print("Density", density)

        boxSize = self.domainSize/self.numberOfBoxes

        boxes = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=np.ndarray)
        volumes = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=float)
        # numTestPoints = density*numTestPoints
        # numTestPoints = numTestPoints.astype(int)
        boxesindices = np.array(np.meshgrid(*[range(self.numberOfBoxes)]*self.dim)).T.reshape(-1, self.dim)
        for indices in boxesindices:
            indicesArr = indices
            # print(indices)
            if len(indices) == 1:
                indices = indices[0]
            else:
                indices = tuple(indices)
            pointsInBox = max(1, int(round(density[indices]*self.numTestPoints)))
            pointsPerDirection = int(pointsInBox**(1/self.dim))
            directpointsInBox = int(pointsPerDirection**self.dim)

            # Generate the random points, that don't fit in the grid
            box = np.random.rand((pointsInBox-directpointsInBox), self.dim)*boxSize
            if shift:
                box += np.array(indicesArr*boxSize)

            # Generate the stratified grid-points
            if pointsPerDirection > 0:
                # Generate the even grid
                linspaces = [np.linspace((i*boxSize), ((i+1)*boxSize), pointsPerDirection, endpoint=False) for i in indices]
                box1 = np.array(np.meshgrid(*linspaces)).T.reshape(-1, self.dim)
                # Now move (stratify) the grid-points
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
        density = np.ones([self.numberOfBoxes] * self.dim)
        self.generateAdaptiveStratifiedGrid(density=density)

    def generateUniformGrid(self):
        '''
        Generates uniform grid with ~'numTestPoints'
        '''
        density = np.ones([self.numberOfBoxes] * self.dim)
        self.generateAdaptiveStratifiedGrid(density=density, shift=False)

    def generateAdaptiveUniformGrid(self, density):
        '''
        Generates uniform adaptive grid with ~'numTestPoints'
        according to the density distribution 'density'
        '''
        self.generateAdaptiveStratifiedGrid(density=density, shift=False)

    def getFlatTestPoints(self):
        d = self.dim
        a = self.testPointPos
        while d > 0:
            a = np.concatenate(a, axis=0)
            d -= 1
        return a
