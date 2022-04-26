# !/usr/bin/python

# AdditionsQt
from click import progressbar
from additionsQt import *
# Threads
from Threads import *
# import Classes
from additionsQt import *

import datetime
# Sound package
from scipy.io import wavfile
from mutagen.wave import WAVE

# Definition of Main Color Palette
from Defs import COLOR1,COLOR2,COLOR3,COLOR4, COLOR5

# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from errorMap import MplCanvasErrorMap
from plotterMatplotlib import MplCanvasPlotter

# importing numpy and pandas
import numpy as np
import pandas as pd

# importing pyqtgraph as pg
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import *

# importing sys package
import sys
import os

# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=logging.INFO)


class Window(QMainWindow):
    """Main Window."""
    def __init__(self):

        """Initializer."""
        super().__init__()
        logging.debug("Application started")

        # Initialize Variable

        # setting Icon
        self.setWindowIcon(QIcon('images/icon.ico'))

        # setting  the fixed width of window
        # width = 1400
        # height = 800
        # self.setMinimumSize(width,height)

        # setting title
        self.setWindowTitle("Musical Instruments Equalizer")

        # UI contents
        self.createMenuBar()

        self.initUI()

        # Status Bar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(f"""font-size:13px;
                                 padding: 3px;
                                 color: {COLOR1};
                                 font-weight:900;""")
        self.statusBar.showMessage("Welcome to our application...")
        self.setStatusBar(self.statusBar)

        # Connect action
        self.connect()
    

    def setTheme(self, theme):
        self.mainPlot.setMode(theme)
        self.errorMapPlot.setMode(theme)

    # Menu
    def createMenuBar(self):
        # MenuBar
        menuBar = self.menuBar()

        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)

        # Open file in menu
        self.openFile = QAction("Open...",self)
        self.openFile.setShortcut("Ctrl+o")
        self.openFile.setStatusTip('Open a new signal')

        fileMenu.addAction(self.openFile)

        # Exit file in menu
        self.quit = QAction("Exit",self)
        self.quit.setShortcut("Ctrl+q")
        self.quit.setStatusTip('Exit application')

        fileMenu.addAction(self.quit)

        # Add file tab to the menu
        menuBar.addMenu(fileMenu)

        logging.info("Menubar has created.")

    # GUI
    def initUI(self):
        centralMainWindow = QWidget(self)
        self.setCentralWidget(centralMainWindow)

        # Outer Layout
        outerLayout = QVBoxLayout()

        ######### INIT GUI #########
        # Main layout
        mainLayout = QHBoxLayout()
        
        panelGroupBox = QGroupBox("Main Panel")
        mainPanel = QVBoxLayout()
        panelGroupBox.setLayout(mainPanel)
        
        # Efficiency Text Box
        self.efficiencyBox = QSpinBox(self)
        self.efficiencyBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")

        # Num. of chunks Text Box
        self.noChunksBox = QSpinBox(self)
        self.noChunksBox.setStyleSheet(f"""font-size:14px; 
                                padding: 5px 15px; 
                                background: {COLOR4};
                                color: {COLOR1};""")

        # Polynomial Degree Text Box
        self.degreeBox = QSpinBox(self)
        self.degreeBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")

        # Overlap Degree Text Box
        self.overlapBox = QSpinBox(self)
        self.overlapBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")

        mainPanel.addWidget(self.efficiencyBox)
        mainPanel.addWidget(self.noChunksBox)
        mainPanel.addWidget(self.degreeBox)
        mainPanel.addWidget(self.overlapBox)

        # Main Plot
        plotLayout = QVBoxLayout()
        latex = QLineEdit()
        self.mainPlot = MplCanvasPlotter("Main Plot")
        plotLayout.addWidget(latex,1)
        plotLayout.addWidget(self.mainPlot,10)

        mainLayout.addWidget(panelGroupBox,3)
        mainLayout.addLayout(plotLayout,7)

        # Error map Layout
        mapLayout = QHBoxLayout()
        
        mapGroupBox = QGroupBox("Error Map Panel")
        mapPanelLayout = QVBoxLayout()
        mapGroupBox.setLayout(mapPanelLayout)

        # X-axis
        xAxisGroupBox = QGroupBox("X-axis")
        xAxisLayout = QHBoxLayout()
        xAxisGroupBox.setLayout(xAxisLayout)

        xAxisOverLap = QRadioButton("Overlap")
        xAxisDegree = QRadioButton("Degree")
        xAxisChunks = QRadioButton("no. of Chunks") 
        
        xAxisLayout.addWidget(xAxisOverLap)
        xAxisLayout.addWidget(xAxisDegree)
        xAxisLayout.addWidget(xAxisChunks)

        # Y-axis
        yAxisGroupBox = QGroupBox("Y-axis")
        yAxisLayout = QHBoxLayout()
        yAxisGroupBox.setLayout(yAxisLayout)

        yAxisOverLap = QRadioButton("Overlap")
        yAxisDegree = QRadioButton("Degree")
        yAxisChunks = QRadioButton("no. of Chunks") 
        
        yAxisLayout.addWidget(yAxisOverLap)
        yAxisLayout.addWidget(yAxisDegree)
        yAxisLayout.addWidget(yAxisChunks)

        mapPanelLayout.addWidget(xAxisGroupBox)
        mapPanelLayout.addWidget(yAxisGroupBox)

        # Error Map Plot
        leftLayout = QVBoxLayout()
        ErrorPrecent = QLineEdit("%")
        self.errorMapPlot = MplCanvasErrorMap("Error Map")
        progressLayout = QHBoxLayout()
        
        progressbar = QProgressBar()
        ButtonProgressBar = QPushButton("Start")

        progressLayout.addWidget(progressbar,10)
        progressLayout.addWidget(ButtonProgressBar,2)

        leftLayout.addWidget(ErrorPrecent)
        leftLayout.addWidget(self.errorMapPlot)
        leftLayout.addLayout(progressLayout)
        
        mapLayout.addWidget(mapGroupBox, 3)
        mapLayout.addLayout(leftLayout ,7)

        outerLayout.addLayout(mainLayout)
        outerLayout.addLayout(mapLayout)
        ######### INIT GUI #########

        centralMainWindow.setLayout(outerLayout)

    # Connect actions
    def connect(self):
        pass

    # Exit the application
    def exit(self):
        exitDlg = QMessageBox.critical(self,
        "Exit the application",
        "Are you sure you want to exit the application?",
        buttons=QMessageBox.Yes | QMessageBox.No,
        defaultButton=QMessageBox.No)

        if exitDlg == QMessageBox.Yes:
            # Exit the application
            sys.exit()

