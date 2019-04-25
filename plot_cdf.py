# -*- coding: utf-8 -*-
"""
    Take as input a list of files, and plot average CDF.
    You can select the x-axis to be either absolution simulation time, or sync
    delay.

    @Author jonnykong@cs.ucla.edu
    @Date   2019-04-09
"""

from __future__ import print_function
import sys
import numpy as np
import matplotlib.pyplot as plt

class CdfPlotter(object):
    """
    This class takes as input a list of filenames, calculate their average, and
    plot the averaged CDF, or save it to disk.
    """
    def __init__(self):
        """
        Initializes default x range to [0, 2400], and assume there are 20 nodes
        in total.
        """
        self._filenames = []
        self._x_mesh = np.linspace(0, 2400, num=2400+1)
        self._node_num = 20
        self._ys_mesh = []   # 2D array

    def add_file(self, filename):
        """
        Add a new file and parse the output.
        """
        self._filenames.append(filename)
        self._parse_file(filename, plot_delay=True)

    def plot_cdf(self, save=False):
        """
        Calculate the mean of self._ys_mesh and draw CDF graph, or save the graph
        to "tmp.png".
        Args:
            save (bool): Save the output graph to disk, rather than displaying it
                on the screen (e.g. if you are working on a remote server).
        """
        y_mean = [float(sum(l)) / len(l) for l in zip(*self._ys_mesh)]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self._x_mesh, y_mean)
        plt.ylim((0, 1))
        if save:
            fig_name = "tmp.png"
            print("Plot saved to %s" % fig_name)
            fig.savefig(fig_name)
        else:
            plt.show()

    def _parse_file(self, filename, plot_delay=True):
        """
        Read one file and interpolate its values. Then, normalize the values
        to [0, 1] and add to self._ys_mesh.
        Args:
            plot_delay (bool): Plot with x-axis being the delay, rather than the
                absolute time of the simulation. This means all data are produced
                at time 0, so data generation time does not reflect on the graph.
        """
        x_coord = []
        data_store = set()
        generated_time = dict()
        with open(filename, "r") as f:
            for line in f.readlines():
                if line.find("Store New Data") == -1:
                    continue
                # if line.find("Update New Seq") == -1:
                #     continue
                elements = line.strip().split(' ')
                time = elements[0]
                data = elements[-1]
                if data not in data_store:
                    data_store.add(data)
                    generated_time[data] = int(time)
                if plot_delay:
                    x_coord.append((int(time) - generated_time[data]) / 1000000)
                else:
                    x_coord.append(int(time) / 1000000)
        y_mesh = self._interp0d(x_coord)
        y_mesh = [float(l / (len(data_store) * self._node_num)) for l in y_mesh]
        self._ys_mesh.append(y_mesh)
        print("Avail: %f" % y_mesh[-1])

    def _interp0d(self, x_coord):
        """
        0-d interpolation against self._x_mesh
        """
        y_interp0d = [0 for i in range(len(self._x_mesh))]
        for i, _ in enumerate(x_coord):
            y_interp0d[int(x_coord[i])] += 1
        for i in range(1, len(y_interp0d)):
            y_interp0d[i] += y_interp0d[i - 1]

        return y_interp0d



if __name__ == "__main__":
    plotter = CdfPlotter()
    for arg in sys.argv[1:]:
        plotter.add_file(arg)
    plotter.plot_cdf(save=True)
