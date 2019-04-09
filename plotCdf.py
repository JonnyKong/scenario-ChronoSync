# -*- coding: utf-8 -*-
"""
    Take as input a list of files, and plot average CDF.
    @Author jonnykong@cs.ucla.edu
    @Date   2019-04-09
"""

import os, sys
import fileinput
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.stats as stats

class CDFPlotter:

    def __init__(self):
        self._filenames = []
        # Default x limit: 0-2400
        self._x = np.linspace(0, 2400, num = 2400 + 1)
        # Default y limit: 400 * 20
        self._y_lim = 400 * 20
        self._y = []    # 1D array
        self._ys = []   # 2D array

    # Add a new file and parse the output
    def addFile(self, filename):
        self._filenames.append(filename)
        self._parseFile(filename)

    # Calculate the mean of self._ys and draw CDF graph
    def plotCdf(self):
        self._y = [float(sum(l)) / len(l) for l in zip(*self._ys)]
        self._y = [float(l / self._y_lim) for l in self._y]
        plt.plot(self._x, self._y)
        plt.ylim((0, 1))
        plt.show()

    # Read one file, interpolate its values and add to self._ys
    def _parseFile(self, filename):
        x = []
        y = []
        with open(filename, "r") as f:
            for line in f.readlines():
                if line.find("Store New Data") == -1:
                    continue
                elements = line.strip().split(' ')
                time = elements[0]
                x.append(int(time) / 1000000)
        self._ys.append(self._interp0d(x))

    # 0-d interpolation according to self._x
    def _interp0d(self, x):
        y_interp0d = [0 for i in range(len(self._x))]
        for i in range(len(x)):
            y_interp0d[int(x[i])] += 1
        for i in range(1, len(y_interp0d)):
            y_interp0d[i] += y_interp0d[i - 1]
        return y_interp0d



if __name__ == "__main__":
    plotter = CDFPlotter()
    for arg in sys.argv[1:]:
        plotter.addFile(arg)
    plotter.plotCdf()
