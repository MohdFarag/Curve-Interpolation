# !/usr/bin/python

# AdditionsQt
from click import progressbar
from sympy import true
from additionsQt import *
# Threads
from Threads import *
# import Classes
from additionsQt import *

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
        self.mainDataPlot = np.array([])
        self.timePlot = np.array([])
        
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
        self.openFile.triggered.connect(self.browseSignal)


        fileMenu.addAction(self.openFile)

        # Exit file in menu
        self.quit = QAction("Exit",self)
        self.quit.setShortcut("Ctrl+q")
        self.quit.setStatusTip('Exit application')

        fileMenu.addAction(self.quit)

        # Add file tab to the menu
        menuBar.addMenu(fileMenu)
        
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
        efficiencyLayout = QVBoxLayout()
        efficiencyLabel = QLabel("Efficiency")
        self.efficiencyBox = QSpinBox(self)
        self.efficiencyBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        efficiencyLayout.addWidget(efficiencyLabel,1)
        efficiencyLayout.addWidget(self.efficiencyBox,5)

        # Num. of chunks Text Box
        noChunksLayout = QVBoxLayout()
        noChunksLabel = QLabel("Num. of chunks")
        self.noChunksBox = QSpinBox(self)
        self.noChunksBox.setStyleSheet(f"""font-size:14px; 
                                padding: 5px 15px; 
                                background: {COLOR4};
                                color: {COLOR1};""")
        noChunksLayout.addWidget(noChunksLabel,1)
        noChunksLayout.addWidget(self.noChunksBox,5)

        # Polynomial Degree Text Box
        degreeLayout = QVBoxLayout()
        degreeLabel = QLabel("Polynomial Degree")
        self.degreeBox = QSpinBox(self)
        self.degreeBox.setMinimum(1)
        self.degreeBox.setMaximum(5)
        self.degreeBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        degreeLayout.addWidget(degreeLabel,1)
        degreeLayout.addWidget(self.degreeBox,5)

        # Overlap Text Box
        overlapLayout = QVBoxLayout()
        overlapLabel = QLabel("Overlap")
        self.overlapBox = QSpinBox(self)
        self.overlapBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        overlapLayout.addWidget(overlapLabel,1)
        overlapLayout.addWidget(self.overlapBox,5)

        mainPanel.addLayout(efficiencyLayout)
        mainPanel.addLayout(noChunksLayout)
        mainPanel.addLayout(degreeLayout)
        mainPanel.addLayout(overlapLayout)

        # Main Plot
        plotLayout = QVBoxLayout()
        
        latex = QLineEdit()
        latex.setStyleSheet("padding:3px; font-size:15px;")
        latex.setDisabled(True)

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
        xAxisOverLap.clicked.connect(lambda: self.xAxisChange(xAxisOverLap.text()))
        xAxisDegree = QRadioButton("Degree")
        xAxisDegree.clicked.connect(lambda: self.xAxisChange(xAxisDegree.text()))
        xAxisChunks = QRadioButton("no. of Chunks")
        xAxisChunks.clicked.connect(lambda: self.xAxisChange(xAxisChunks.text()))

        # X Axis Input range
        self.xFrame = QFrame()
        xAxisRange = QHBoxLayout()
        self.xFrame.setLayout(xAxisRange)
        self.xAxisLabel = QLabel("Overlap")
        xAxisInput = QLineEdit()
        xAxisRange.addWidget(self.xAxisLabel)
        xAxisRange.addWidget(xAxisInput)
        self.xFrame.hide()
        
        xAxisLayout.addWidget(xAxisOverLap)
        xAxisLayout.addWidget(xAxisDegree)
        xAxisLayout.addWidget(xAxisChunks)

        # Y-axis
        yAxisGroupBox = QGroupBox("Y-axis")
        yAxisLayout = QHBoxLayout()
        yAxisGroupBox.setLayout(yAxisLayout)

        yAxisOverLap = QRadioButton("Overlap")
        yAxisOverLap.clicked.connect(lambda: self.yAxisChange(yAxisOverLap.text()))
        yAxisDegree = QRadioButton("Degree")
        yAxisDegree.clicked.connect(lambda: self.yAxisChange(yAxisDegree.text()))
        yAxisChunks = QRadioButton("no. of Chunks")
        yAxisChunks.clicked.connect(lambda: self.yAxisChange(yAxisChunks.text()))
        
        # Y Axis Input range
        self.yFrame = QFrame()
        yAxisRange = QHBoxLayout()
        self.yFrame.setLayout(yAxisRange)
        self.yAxisLabel = QLabel("Overlap")
        yAxisInput = QLineEdit()
        yAxisRange.addWidget(self.yAxisLabel)
        yAxisRange.addWidget(yAxisInput)
        self.yFrame.hide()
        
        yAxisLayout.addWidget(yAxisOverLap)
        yAxisLayout.addWidget(yAxisDegree)
        yAxisLayout.addWidget(yAxisChunks)

        mapPanelLayout.addWidget(xAxisGroupBox)
        mapPanelLayout.addWidget(self.xFrame)
        mapPanelLayout.addWidget(yAxisGroupBox)
        mapPanelLayout.addWidget(self.yFrame)

        # Error Map Plot
        leftLayout = QVBoxLayout()
        
        ErrorPrecent = QLineEdit("%")
        ErrorPrecent.setStyleSheet("padding:3px; font-size:15px;")
        ErrorPrecent.setDisabled(True)

        self.errorMapPlot = MplCanvasErrorMap("Error Map",8,5)
        progressLayout = QHBoxLayout()
        
        progressbar = QProgressBar()
        progressbar.setStyleSheet("padding:2px;")
        ButtonProgressBar = QPushButton("Start")
        ButtonProgressBar.setStyleSheet("padding:2px; font-size:15px;")

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

    def browseSignal(self):
        # Open File
        try:
            path, fileExtension = QFileDialog.getOpenFileName(None, "Load Signal File", os.getenv('HOME') ,"csv(*.csv)")

            if path == "":
                self.timePlot = np.linspace(-10, 10, 1000)
                self.mainDataPlot = np.sin(self.timePlot) + np.sin(2*self.timePlot) + 5*np.sin(3*self.timePlot) + 10*np.sin(6*self.timePlot)
                # return
                    
            if fileExtension == "csv(*.csv)":
                self.mainDataPlot = pd.read_csv(path).iloc[:,1].values.tolist()
                self.timePlot = pd.read_csv(path).iloc[:,0].values.tolist()
        except:
            logging.error("Can't open a csv file")
        self.mainPlot.clearSignal()
        self.mainPlot.set_data(self.mainDataPlot, self.timePlot)
        self.mainPlot.plotSignal()

    # TODO: X AND Y in one function (self, "x or y", value)
    def yAxisChange(self, value):
        self.yFrame.show()
        self.yAxisLabel.setText(value)

    def xAxisChange(self, value):
        self.xFrame.show()
        self.xAxisLabel.setText(value)

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

