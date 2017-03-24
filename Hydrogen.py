# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import BoxPlotter


RESULT_PATH = "simulation_results"
IMAGE_PATH = RESULT_PATH+"/images"


mcer = MCIntegrator.MCIntegrator(dim=3, numTestPoints=1000, domainSize=10, numberOfBoxes=5)

bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)
bplotter.plotBox(True, False)


result, a =mcer.integrate()
print(result)