# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import BoxPlotter


RESULT_PATH = "simulation_results"
IMAGE_PATH = RESULT_PATH+"/images"

def hydrogenTestFunction(pos, dim):
        #return np.sum((pos[:]-5)**2, axis=1)
        numberOfBoxes = len(pos)
        f = np.array(np.zeros([numberOfBoxes]*dim), dtype=np.ndarray)
        f_sum = np.array(np.zeros([numberOfBoxes]*dim), dtype=float)
    
    
        boxesindices = np.array(np.meshgrid(*[range(numberOfBoxes)]*dim)).T.reshape(-1,dim)
        for indices in boxesindices:
            indices=tuple(indices)
            f[indices] = (pos[indices][:,0]-5)**2 + (pos[indices][:,1]-5)**2
            f_sum[indices] = sum(f[indices]) 
    
        return f, f_sum

mcer = MCIntegrator.MCIntegrator(dim=2, numTestPoints=1000, domainSize=10, numberOfBoxes=5, testFunction=hydrogenTestFunction)

bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)
bplotter.plotBox(True, False)


result, a =mcer.integrate()
print(result)