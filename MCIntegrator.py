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
    actNumberOfTestPoints = 0


    def __init__(self, dim, numTestPoints, domainSize, numberOfBoxes):
        self.dim=dim
        self.numTestPoints=numTestPoints
        self.domainSize=domainSize
        self.numberOfBoxes=numberOfBoxes

    def integrate(self, function):
        '''
        The passed function is being integrated over the domain with the
        previously specified grid.
        Returns the total integral, the integral per integration box and the
        normalized integration value per Box.
        '''
        f, functionArraySummed = self._funcWrapper(func=function)
        
        #print("f=",f)
        #print("sum(f)=",functionArraySummed)
        
        boxIntegral = functionArraySummed*self.testPointVol
        pointIntegral = f*self.testPointVol
        totalIntegral = np.sum(boxIntegral)
        newDensity = np.absolute(boxIntegral)/totalIntegral
        
        return totalIntegral, pointIntegral, newDensity

    def generateAdaptiveStratifiedGrid(self, density, shift=True):
        '''
        Generates a adaptive (according to density, if it is not a matrix of ones)
        and stratified (if shift=True, else a uniform) grid with ~'numTestPoints'.
        '''
        
        #Normalize the density
        density = np.abs(density)
        density /= np.sum(density)

        #Determine the size of each adative grid box
        boxSize = self.domainSize/self.numberOfBoxes

        #Prepare the temporary arrays
        boxes = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=np.ndarray)
        volumes = np.array(np.zeros([self.numberOfBoxes]*self.dim), dtype=float)
        totalPoints=0
        
        #Create the linear superposition of all indices
        boxesindices = np.array(np.meshgrid(*[range(self.numberOfBoxes)]*self.dim)).T.reshape(-1, self.dim)
        
        
        #Fill each box with the according amount of points
        for indices in boxesindices:
            indicesArr = indices
            # print(indices)
            if len(indices) == 1:
                indices = indices[0]
            else:
                indices = tuple(indices)
            
            #Calculate how many test points we need to put in this box
            pointsInBox = max(1, int(round(density[indices]*self.numTestPoints)))
            pointsPerDirection = int(pointsInBox**(1/self.dim))
            totalPoints+=pointsInBox
            #How many points can we put into a grid?
            directpointsInBox = int(pointsPerDirection**self.dim)

            # Generate the random points, that don't fit in the grid
            box = (np.random.rand((pointsInBox-directpointsInBox), self.dim)+indicesArr)*boxSize

            # Generate the (stratified) grid-points
            if pointsPerDirection > 0:
                # Generate the even grid
                linspaces = [np.linspace((i*boxSize), ((i+1)*boxSize), pointsPerDirection, endpoint=False) for i in indicesArr]
                box1 = np.array(np.meshgrid(*linspaces)).T.reshape(-1, self.dim)
                
                
                l = boxSize/pointsPerDirection
                if shift:                
                    # Now move (stratify) the grid-points
                    box1 += np.random.rand(directpointsInBox, self.dim)*l
                else:
                    box1 += l/2
                #Now put the random and the stratified point in the same array
                box = np.concatenate([box1, box])
            
            #Done with this box
            boxes[indices] = box
            volumes[indices] = (boxSize**self.dim)/pointsInBox
        
        #Make sure, that we use numpy arrays and write the class variables.
        boxes = np.array(boxes)
        volumes = np.array(volumes)
        self.testPointPos = boxes
        self.testPointVol = volumes
        self.actNumberOfTestPoints = totalPoints
        return totalPoints

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
        '''
        Returns the test points as simple array
        '''
        return self._flattenArray(self.testPointPos)
        
    def _flattenArray(self, a):
        d = self.dim
        while d > 0:
            a = np.concatenate(a, axis=0)
            d -= 1
        return a

    def _funcWrapper(self, func):
        '''
        Takes a function only of the position and alpha and turns it into a
        function of the postion matrix
        '''
        dim=self.dim
        numberOfBoxes = self.numberOfBoxes
        pos=self.testPointPos
        
        f = np.array(np.zeros([numberOfBoxes]*dim), dtype=np.ndarray)
        f_sum = np.array(np.zeros([numberOfBoxes]*dim), dtype=float)
    
        boxesindices = np.array(np.meshgrid(*[range(numberOfBoxes)]*dim)).T.reshape(-1, dim)
        for indices in boxesindices:
            indices = tuple(indices)
            f[indices] = func(pos=np.array(pos[indices]))
            f_sum[indices] = sum(f[indices])
    
        return f, f_sum