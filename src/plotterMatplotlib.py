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
        
        self.fig = Figure(facecolor=f"{COLOR1}")

        self.axes = self.fig.add_subplot(111)
                
        self.axes.set_title(title, fontweight ="bold", color=f"{COLOR4}")
        self.axes.set_xlabel("Time", color=f"{COLOR4}")
        self.axes.set_ylabel("Amplitude", color=f"{COLOR4}")
        self.axes.set_facecolor(f"{COLOR1}")
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)

        self.axes.spines['bottom'].set_color(f"{COLOR4}")
        self.axes.spines['left'].set_color(f"{COLOR4}")

        self.axes.tick_params(axis='x', colors=f"{COLOR4}")
        self.axes.tick_params(axis='y', colors=f"{COLOR4}")
        
        super(MplCanvasPlotter, self).__init__(self.fig)


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


    def clearSignal(self):
        self.axes.clear()
        self.axes.set_xlim([min(self.x), max(self.x)])
        self.axes.set_ylim([min(self.y), max(self.y)+1])