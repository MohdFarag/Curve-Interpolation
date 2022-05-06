import sys
import os

# matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

# Logging configuration
import logging

from sympy import false
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=os.environ.get("LOGLEVEL", "INFO"))

class MplCanvasErrorMap(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=8, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_edgecolor("white")
            
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title("Error Map", fontweight ="bold")

        # Color bar
        colormap = plt.cm.get_cmap("rainbow")
        sm = plt.cm.ScalarMappable(cmap=colormap)
        self.colorBarSpectrogram = self.fig.colorbar(sm)

        super(MplCanvasErrorMap, self).__init__(self.fig)

    data_channel = [np.random.randint(-10,10) for i in range(500)]
    colorPalette = "rainbow"

    def setMode(self, theme):
        if theme == "Dark":
            # Change color of face color
            self.setFaceColor("#19232d", "#212933")
            # Change color of Texts
            self.setTextColor("#fff")
        elif theme == "Orange":
            # Change color of face color
            self.setFaceColor("#323232", "#212933")
            # Change color of Texts
            self.setTextColor("#fff")

        elif theme == "Light":
            # Change color of face color
            self.setFaceColor("#fff" , "#fff")
            # Change color of Texts
            self.setTextColor("#212933")

    def setTextColor(self,color):
        # Change color of axes border
        self.axes.spines["bottom"].set_color(color)
        self.axes.spines["top"].set_color(color)
        self.axes.spines["right"].set_color(color)
        self.axes.spines["left"].set_color(color)
        # Change color of labels
        self.axes.tick_params(axis='x', colors=color)
        self.axes.tick_params(axis='y', colors=color)
        # Change color bar text color
        plt.setp(plt.getp(self.colorBarSpectrogram.ax.axes, 'yticklabels'), color=color)
        self.colorBarSpectrogram.ax.tick_params(color=color)

    def setFaceColor(self,figColor, axesColor):
        self.fig.set_facecolor(figColor)
        # Change color of axes
        self.axes.set_facecolor(axesColor)

    def addColorBar(self):
        try:
            colormap = plt.cm.get_cmap(self.colorPalette)
            sm = plt.cm.ScalarMappable(cmap=colormap)
            self.colorBarSpectrogram = self.fig.colorbar(sm)
            self.colorBarSpectrogram.solids.set_edgecolor("face")
        except:
            logging.error("Failed to add color bar.")

    def set_color(self, colorPalette):
        self.colorPalette = colorPalette

    def set_data_channel(self, data_channel):
        self.data_channel = data_channel

    def setAxesLabel(self,axes,title):
        if axes=="x":
            self.axes.set_xlabel(title)
        elif axes=="y":
            self.axes.set_ylabel(title)
        else:
            return False

    def plotErrorMap(self):
        self.data_channel = np.array(self.data_channel)

        if self.data_channel.ndim > 1 :
            self.axes.imshow(self.data_channel)
            self.draw()  
        else :
            logging.error("Can't generate image plot because array is 2D.") 

        self.fig.set_size(18, 10, forward=True)  
        
    def clearSignal(self):
        self.axes.clear()