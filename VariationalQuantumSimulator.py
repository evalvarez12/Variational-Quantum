# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import numpy as np
#from functools import partial

class VariationalQuantumSimulator:
    '''

    '''

    ###Functions given by the problem
    testFunction = None
    localEnergyFunction = None
    testFuncDeriv = None

    #Object-handle for the integrator
    integrator = None

    ###Local optimization variables
    #Energy of the test-function
    energy = 0

    #The variational parameter
    alpha = 0

    #The damping constant, between 0 and 1, where
    #0 -> no correction
    #1 -> no damping
    gamma = 1

    #How many iterations have me made so far?
    iterations = 0

    def __init__(self, dim, numTestPoints, domainSize, numberOfBoxes,
                 testFunction, localEnergyFunction, testFuncDeriv, startAlpha, damping):
        #self.dim = dim
        #self.numTestPoints = numTestPoints
        #self.domainSize = domainSize
        #self.numberOfBoxes = numberOfBoxes
        self.testFunction = testFunction
        self.localEnergyFunction = localEnergyFunction
        self.testFuncDeriv = testFuncDeriv
        self.alpha = startAlpha
        self.gamma = damping

        self.integrator = MCIntegrator.MCIntegrator(dim=dim,
            numTestPoints=numTestPoints, domainSize=domainSize, numberOfBoxes=numberOfBoxes)

        self.integrator.generateStratifiedGrid()

    def initializeGrid(self, iterations=5):
        for i in range(iterations):
            totalIntegral, boxIntegral, newDensity = self.integrator.integrate(
            self._getPosDensity)
            self.integrator.generateAdaptiveStratifiedGrid(newDensity)

    def iterate(self, adaptGrid=False):
        '''
        adapting the grid will slow down this function
        '''

        #Calculate the new density and energy
        totalDensity, densityPerBox, normDensityPerBox = self.integrator.integrate(
            self._getPosDensity)

        totalEnergy, energyFunction, _ = self.integrator.integrate(
            self._getPosEnergy)

        self.energy = totalEnergy / totalDensity

        #Calculate the new alpha according to eq. 12.14
        term1, _, _ = self.integrator.integrate(self._getPosLocalEnergyTestFuncDeriv)
        term2, _, _ = self.integrator.integrate(self._getPosTestFuncDeriv)
        dEdA = 2*(term1 - self.energy*term2)

        self.alpha = self.alpha - self.gamma*dEdA

        if adaptGrid:
            self.integrator.generateAdaptiveStratifiedGrid(normDensityPerBox)

        self.iterations += 1

    ##### Get simulation results
    def getIterations(self):
        return self.iterations

    def getAlpha(self):
        return self.alpha

    def getEnergy(self):
        return self.energy


    ##### Wrap and combine all the functions we need!
    ### Base functions
    def _getPosLocalEnergy(self, pos):
        '''
        E_L
        eq. 12.3
        '''
        return self._funcWrapper(func=self.localEnergyFunction, pos=pos, alpha=self.alpha)

    def _getPosTestFunction(self, pos):
        '''
        Psi_T(alpha)
        '''
        return self._funcWrapper(func=self.testFunction, pos=pos, alpha=self.alpha)

    def _getPosTestFuncDeriv(self, pos):
        '''
        d(ln(Psi))/d alpha
        Term two from eq. 12.13, page 378 in the book
        '''
        return self._funcWrapper(func=self.testFuncDeriv, pos=pos, alpha=self.alpha)

    ### Use the previous functions to define a few others
    def _getPosEnergy(self, pos):
        '''
        E * Rho
        ~ eq. 12.4
        '''
        a, b = self._getPosDensity(pos)
        c, d = self._getPosLocalEnergy(pos)
        return a*c, b*d

    def _getPosLocalEnergyTestFuncDeriv(self, pos):
        '''
        E_L * d(ln(Psi))/d alpha
        Term one from eq. 12.13, page 378 in the book
        '''
        a, b = self._getPosLocalEnergy(pos)
        c, d = self._getPosTestFuncDeriv(pos)
        return a*c, b*d

    def _getPosDensity(self, pos):
        '''
        rho = <Psi|Psi>
        '''
        a, b = self._getPosTestFunction(pos)
        return a**2, b**2

    def _funcWrapper(self, func, pos, alpha):
        '''
        Takes a function only of the position and alpha and turns it into a
        function of the postion matrix
        '''
        numberOfBoxes = len(pos)
        dim = len(pos[0][0])
        f = np.array(np.zeros([numberOfBoxes]*dim), dtype=np.ndarray)
        f_sum = np.array(np.zeros([numberOfBoxes]*dim), dtype=float)

        boxesindices = np.array(np.meshgrid(*[range(numberOfBoxes)]*dim)).T.reshape(-1, dim)
        for indices in boxesindices:
            indices = tuple(indices)
            f[indices] = func(np.array(pos[indices]), alpha)
            f_sum[indices] = np.sum(f[indices])

        return f, f_sum
