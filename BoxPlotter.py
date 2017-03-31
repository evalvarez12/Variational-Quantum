#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Plotting packages
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations


# Other packages
from pathlib import Path
import numpy as np


class BoxPlotter:
    RESULT_PATH = "simulation_results"
    IMAGE_PATH = RESULT_PATH+"/images"
    VIDEO_DESC_FILE = ""
    sim = 0
    plotSize = 8
    plots = 0

    def __init__(self, sim, RESULT_PATH, IMAGE_PATH):
        self.RESULT_PATH = RESULT_PATH
        self.IMAGE_PATH = IMAGE_PATH
        self.sim = sim

        path = Path(self.IMAGE_PATH)
        try:
            if not path.exists():
                path.mkdir(parents=True)
        except OSError:
            print("Image path could not be created")


    '''
    Plots the atoms and their vectors inside the Box
    '''
    def plotBox(self, show=False, write=True):
        if self.sim.dim == 1:
            self._plotBox1D(show, write)
        elif self.sim.dim == 2:
            self._plotBox2D(show, write)
        else:
            self._plotBox3D(show, write)

    '''
    PRIVATE - do not call from outside
    Generates a plot title
    '''
    def _getPlotTitle(self):
        # Create the figure title
        it = "I: %05.f" % self.sim.iterations
        energy = ", E=%.3f" % self.sim.getEnergy()
        title = it+energy
        return title

    '''
    PRIVATE - do not call from outside
    Displays into the console and writes the latest plots into a png
    '''
    def _showWritePlotFile(self, plt, show=False, write=True):
        if (show or write):
            plt.draw()
            plt.title(self._getPlotTitle())

            # You could alternatively use
            # pic = frame_%05d.png' % (self.iterations);
            # to get a fixed five-digit output for the iteration number
            if write:
                pic = 'frame_' + str(self.plots) + '.png'
                plt.savefig(self.IMAGE_PATH+"/"+pic, box_inches='tight', dpi=100)
                self.VIDEO_DESC_FILE.write("file "+pic+"\n")
                self.VIDEO_DESC_FILE.write("duration %.3f\n" % (self.pastTimeSinceLastPlot*20))
                self.VIDEO_DESC_FILE.flush()

            if show:
                plt.show()

            plt.close()

    # PRIVATE - do not call from outside
    def _plotBox1D(self, show=False, write=True):
        if self.sim.dim == 1:
            plt.figure()

            ax = plt.gca()
            ax.set_xlim([0, self.sim.domainSize])
            ax.set_ylim([0, 2])
            ax.set_aspect('equal')
            plt.rcParams["figure.figsize"] = [self.plotSize, 2/self.sim.domainSize]

            # Ploting in 2D
            v = self.sim.getFlatTestPoints()
            plt.plot(v[:, 0], 1, 'r.')

            self._showWritePlotFile(plt, show, write)
        else:
            print("Dimensionality not correct! Please call 'plotBox()' instead!")

    # PRIVATE - do not call from outside
    def _plotBox2D(self, show=False, write=True):
        if self.sim.dim == 2:
            plt.figure()

            ax = plt.gca()
            ax.set_xlim([0, self.sim.domainSize])
            ax.set_ylim([0, self.sim.domainSize])
            ax.set_aspect('equal')
            plt.rcParams["figure.figsize"] = [self.plotSize]*2

            # Ploting in 2D
            v = self.sim.getFlatTestPoints()
            plt.plot(v[:, 0], v[:, 1], 'r.')

            self._showWritePlotFile(plt, show, write)
        else:
            print("Dimensionality not correct! Please call 'plotBox()' instead!")

    # PRIVATE - do not call from outside
    def _plotBox3D(self, show=False, write=True):
        if self.sim.dim == 3:
            fig = plt.figure()

            ax = fig.gca(projection='3d')
            ax.set_xlim([0, self.sim.domainSize])
            ax.set_ylim([0, self.sim.domainSize])
            ax.set_zlim([0, self.sim.domainSize])
            ax.set_aspect("equal")
            plt.rcParams["figure.figsize"] = [self.plotSize]*2

            # draw cube
            for s, e in combinations(np.array(list(product(*[[0, self.sim.domainSize]]*3))), 2):
                i=0
                if s[0] == e[0]:
                    i += 1
                if s[1] == e[1]:
                    i += 1
                if s[2] == e[2]:
                    i += 1
                if i == 2:
                    ax.plot3D(*zip(s, e), color="k")

            # draw points
            v = self.sim.getFlatTestPoints()
            ax.scatter(v[:, 0], v[:, 1], v[:, 2], color="r", s=20)

            fig.set_size_inches(self.plotSize, self.plotSize)

            self._showWritePlotFile(plt, show, write)
        else:
            print("Dimensionality not correct! Please call 'plotBox()' instead!")
