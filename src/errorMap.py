import sys
import os

# matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvas
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Logging configuration
import logging

from sympy import false
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

    def set_size(self, w, h):
        
        """ w, h: width, height in inches """
        l = self.fig.subplotpars.left
        r = self.fig.subplotpars.right
        t = self.fig.subplotpars.top
        b = self.fig.subplotpars.bottom
        
        figw = float(w)/(r-l)
        figh = float(h)/(t-b)
        
        self.fig.set_size_inches(figw, figh)

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
            # self.set_size(8,5)
            # self.fig.set_figwidth(8)
            # self.fig.set_figheight(5)
        else :
            logging.error("Can't generate image plot because array is 2D.") 
        
    def clearSignal(self):
        self.axes.clear()

class MatplotlibWidget(QWidget):
    """
    Implements a Matplotlib figure inside a QWidget.
    Use getFigure() and redraw() to interact with matplotlib.
    
    Example::
    
        mw = MatplotlibWidget()
        subplot = mw.getFigure().add_subplot(111)
        subplot.plot(x,y)
        mw.draw()
    """
    
    def __init__(self, size=(5.0, 4.0), dpi=100):
        QWidget.__init__(self)
        self.fig = Figure(size, dpi=dpi)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setParent(self)
        
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.canvas)
        
        self.setLayout(self.vbox)

    def getFigure(self):
        return self.fig
        
    def draw(self):
        self.canvas.draw()