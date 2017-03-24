# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:59:19 2017

@author: rene
"""

import MCIntegrator
import BoxPlotter


RESULT_PATH = "simulation_results"
IMAGE_PATH = RESULT_PATH+"/images"


mcer = MCIntegrator.MCIntegrator()
mcer.integrate()

bplotter = BoxPlotter.BoxPlotter(mcer, RESULT_PATH, IMAGE_PATH)
bplotter.plotBox(True, False)
