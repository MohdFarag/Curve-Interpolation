import sys
import os

# matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=os.environ.get("LOGLEVEL", "INFO"))

class MplCanvasErrorMap(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.fig.set_edgecolor("white")
        self.axes = self.fig.add_subplot(111)

        self.dataMeas = np.array([])
        self.colorBarSpectrogram = None  # Initialize color bar as None
        super(MplCanvasErrorMap, self).__init__(self.fig)

    data_channel = [np.random.randint(-10,10) for i in range(500)]
    colorPalette = "viridis"

    def setMode(self, theme):
        if theme == "Dark":
            self.setFaceColor("#19232d", "#212933")
            self.setTextColor("#fff")
        elif theme == "Orange":
            self.setFaceColor("#323232", "#212933")
            self.setTextColor("#fff")
        elif theme == "Light":
            self.setFaceColor("#fff" , "#fff")
            self.setTextColor("#212933")

    def setTextColor(self, color):
        self.axes.spines["bottom"].set_color(color)
        self.axes.spines["top"].set_color(color)
        self.axes.spines["right"].set_color(color)
        self.axes.spines["left"].set_color(color)
        self.axes.tick_params(axis='x', colors=color)
        self.axes.tick_params(axis='y', colors=color)
        if self.colorBarSpectrogram:
            plt.setp(plt.getp(self.colorBarSpectrogram.ax.axes, 'yticklabels'), color=color)
            self.colorBarSpectrogram.ax.tick_params(color=color)

    def setFaceColor(self, figColor, axesColor):
        self.fig.set_facecolor(figColor)
        self.axes.set_facecolor(axesColor)

    def set_color(self, colorPalette):
        self.colorPalette = colorPalette

    def set_data_channel(self, data_channel):
        self.data_channel = data_channel

    def set_size(self, w, h):
        left = self.fig.subplotpars.left
        right = self.fig.subplotpars.right
        top = self.fig.subplotpars.top
        bottom = self.fig.subplotpars.bottom

        figw = float(w) / (right - left)
        figh = float(h) / (top - bottom)

        self.fig.set_size_inches(figw, figh)

    def setAxesLabel(self, axes, title):
        if axes == "x":
            self.axes.set_xlabel(title)
        elif axes == "y":
            self.axes.set_ylabel(title)
        else:
            return False

    def plotErrorMap(self):
        self.data_channel = np.array(self.data_channel)
        if self.data_channel.ndim > 1:
            self.dataMeas = self.axes.imshow(self.data_channel, interpolation="none", resample=True,
                                             cmap=self.colorPalette, vmin=0, vmax=100,
                                             extent=[0, self.data_channel.shape[1], 0, self.data_channel.shape[0]])
            self.axes.set_aspect(self.data_channel.shape[1] / (self.data_channel.shape[0] * 2))

            if not self.colorBarSpectrogram:
                colormap = plt.cm.get_cmap(self.colorPalette)
                sm = plt.cm.ScalarMappable(cmap=colormap)
                self.colorBarSpectrogram = self.fig.colorbar(sm, ax=self.axes)

            self.colorBarSpectrogram.update_normal(self.dataMeas)
            self.draw()
        else:
            logging.error("Can't generate image plot because array is not 2D.")

    def clearSignal(self):
        self.axes.clear()