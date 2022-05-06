# importing Qt widgets
from turtle import color
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from scipy import signal
from scipy.special import sinc


# Definition of Main Color Palette
from Defs import COLOR1, COLOR2, COLOR3, COLOR4, COLOR5

# importing numpy and pandas
import numpy as np
import pandas as pd

# matplotlib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from random import randint

class MplCanvasPlotter(FigureCanvasQTAgg):
    
    def __init__(self, parent=None,title="Signal Plot"):
        
        self.y = [0]
        self.x = np.linspace(-np.pi/2, np.pi/2, 1000)
        self.sampling = 1
        self.sampledTime, self.sampledSignal = [],[]
        
        self.fig = Figure()

        self.axes = self.fig.add_subplot(111)
                
        self.axes.set_title(title, fontweight ="bold")
        
        super(MplCanvasPlotter, self).__init__(self.fig)

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

    def setFaceColor(self,figColor, axesColor):
        self.fig.set_facecolor(figColor)
        # Change color of axes
        self.axes.set_facecolor(axesColor)

    def set_data(self, y, x, sampling=1 ,sampledTime=[], sampledSignal=[]):
        self.y = y
        self.x = x
        
        self.sampledTime = sampledTime 
        self.sampledSignal = sampledSignal
        self.sampling = sampling

    def plotSignal(self):
        self.clearSignal()
        self.axes.plot(self.x, self.y)
        self.draw()

    def plotChunks(self,x, y):
        self.axes.plot(x, y)
        self.draw()

    def clearChunks(self):
        self.clearSignal()
        self.plotSignal()

    def clearSignal(self):
        self.axes.clear()
        self.axes.set_xlim([min(self.x), max(self.x)])
        self.axes.set_ylim([min(self.y), max(self.y)+1])