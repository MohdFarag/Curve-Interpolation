# !/usr/bin/python

# AdditionsQt
from cProfile import label
import chunk
import string

from sympy import degree, true
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

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

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

        ### Initialize Variable
        self.mainDataPlot = np.array([])
        self.timePlot = np.array([])
        
        # interpolation variables
        self.overlap = 0
        self.precentage = 100
        self.noChunks = 1
        self.degree = 1
        self.latexList = list()
        
        # Error map variables
        self.yErrorMap = ""
        self.xErrorMap = ""

        ### Setting Icon
        self.setWindowIcon(QIcon('images/icon.ico'))

        # Setting  the fixed width of window
        # width = 1400
        # height = 800
        # self.setMinimumSize(width,height)

        ### Setting title
        self.setWindowTitle("Musical Instruments Equalizer")

        ### UI contents
        self.createMenuBar()

        self.initUI()

        ### Status Bar
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(f"""font-size:13px;
                                 padding: 3px;
                                 color: {COLOR1};
                                 font-weight:900;""")
        self.statusBar.showMessage("Welcome to our application...")
        self.setStatusBar(self.statusBar)

        ### Connect action
        self.connect()
    
    # Set theme
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

        # Num. of chunks Text Box
        noChunksLayout = QVBoxLayout()
        noChunksLabel = QLabel("Num. of chunks")
        self.noChunksBox = QSpinBox(self)
        self.noChunksBox.setMinimum(1)
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
        self.degreeBox.setMaximum(8)
        self.degreeBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        degreeLayout.addWidget(degreeLabel,1)
        degreeLayout.addWidget(self.degreeBox,5)

        # Overlap Text Box
        overlapLayout = QVBoxLayout()
        overlapLabel = QLabel("Overlap %")
        
        overlapBoxLayout = QHBoxLayout()
        self.overlapBox = QSpinBox(self)
        self.overlapBox.setMinimum(0)
        self.overlapBox.setMaximum(25)
        self.overlapBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        overlapBoxLayout.addWidget(self.overlapBox, 20)
        overlapBoxLayout.addWidget(QLabel("%"), 1)
        
        overlapLayout.addWidget(overlapLabel,1)
        overlapLayout.addLayout(overlapBoxLayout,5)

        # Overlap Text Box
        precentageLayout = QVBoxLayout()
        precentageLabel = QLabel("Efficiency %")
        
        sliderLayout = QHBoxLayout()
        self.precentageSlider = QSlider(Qt.Horizontal)
        self.precentageSlider.setMinimum(0)
        self.precentageSlider.setMaximum(100)
        self.precentageSlider.setValue(100)
        
        self.precentageCount = QLabel("100%")
        sliderLayout.addWidget(self.precentageSlider,10)
        sliderLayout.addWidget(self.precentageCount,1)

        precentageLayout.addWidget(precentageLabel,1)
        precentageLayout.addLayout(sliderLayout,5)

        mainPanel.addLayout(noChunksLayout)
        mainPanel.addLayout(degreeLayout)
        mainPanel.addLayout(overlapLayout)
        mainPanel.addLayout(precentageLayout)

        # Main Plot
        plotLayout = QVBoxLayout()
        
        latexLayout = QHBoxLayout()
        self.chunksList = QComboBox()
        self.chunksList.setStyleSheet("padding:2px; font-size:15px;")
        self.chunksList.addItem("no.")
        self.latex = QLabel("")
        self.latex.setStyleSheet("padding:5px")
        latexLayout.addWidget(self.latex,20)
        latexLayout.addWidget(self.chunksList,2)

        self.mainPlot = MplCanvasPlotter("Main Plot")
        plotLayout.addLayout(latexLayout ,1)
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

        self.xAxisOverLap = QRadioButton("Overlap")
        self.xAxisDegree = QRadioButton("Degree")
        self.xAxisChunks = QRadioButton("No. of Chunks")
        
        xAxisLayout.addWidget(self.xAxisOverLap)
        xAxisLayout.addWidget(self.xAxisDegree)
        xAxisLayout.addWidget(self.xAxisChunks)

        # Y-axis
        yAxisGroupBox = QGroupBox("Y-axis")
        yAxisLayout = QHBoxLayout()
        yAxisGroupBox.setLayout(yAxisLayout)

        self.yAxisOverLap = QRadioButton("Overlap")
        self.yAxisDegree = QRadioButton("Degree")
        self.yAxisChunks = QRadioButton("No. of Chunks")        
        
        yAxisLayout.addWidget(self.yAxisOverLap)
        yAxisLayout.addWidget(self.yAxisDegree)
        yAxisLayout.addWidget(self.yAxisChunks)

        mapPanelLayout.addWidget(xAxisGroupBox)
        mapPanelLayout.addWidget(yAxisGroupBox)

        # Error Map Plot
        leftLayout = QVBoxLayout()
        
        self.ErrorPrecent = QLineEdit("%")
        self.ErrorPrecent.setStyleSheet("padding:3px; font-size:15px;")
        self.ErrorPrecent.setDisabled(True)

        self.errorMapPlot = MplCanvasErrorMap("Error Map",8,5)
        progressLayout = QHBoxLayout()
        
        progressbar = QProgressBar()
        progressbar.setStyleSheet("padding:2px;")
        self.ButtonProgressBar = QPushButton("Start")
        self.ButtonProgressBar.setStyleSheet("padding:2px; font-size:15px;")

        progressLayout.addWidget(progressbar,10)
        progressLayout.addWidget(self.ButtonProgressBar,2)

        leftLayout.addWidget(self.ErrorPrecent)
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
        self.chunksList.currentTextChanged.connect(lambda: self.chunkLatexChange(self.chunksList.currentText()))

        self.noChunksBox.valueChanged.connect(lambda: self.changeNoChunks(self.noChunksBox.value()))
        self.overlapBox.valueChanged.connect(lambda: self.changeOverLap(self.overlapBox.value()))
        self.precentageSlider.valueChanged.connect(lambda: self.changePrecentage(self.precentageSlider.value()))
        self.degreeBox.valueChanged.connect(lambda: self.changeDegree(self.degreeBox.value()))

        # Error map
        self.ButtonProgressBar.clicked.connect(lambda: self.generateErrorMap())

        self.xAxisOverLap.clicked.connect(lambda: self.xAxisChange(self.xAxisOverLap.text()))
        self.xAxisDegree.clicked.connect(lambda: self.xAxisChange(self.xAxisDegree.text()))
        self.xAxisChunks.clicked.connect(lambda: self.xAxisChange(self.xAxisChunks.text()))

        self.yAxisOverLap.clicked.connect(lambda: self.yAxisChange(self.yAxisOverLap.text()))
        self.yAxisDegree.clicked.connect(lambda: self.yAxisChange(self.yAxisDegree.text()))
        self.yAxisChunks.clicked.connect(lambda: self.yAxisChange(self.yAxisChunks.text()))

    def chunkLatexChange(self, i):
        # Update label
        try:
            latexPixmap = self.latexToLabel(self.latexList[int(i)-1],15)
            # Update latex text
            self.latex.setPixmap(latexPixmap)
        except: 
            pass
    
    def changePrecentage(self,value):
        self.precentageCount.setText(str(value)+'%')
        self.precentage = value
        self.updateAfterEveryChange()
    
    def changeOverLap(self,value):
        self.overlap = value
        self.updateAfterEveryChange()
    
    def changeDegree(self,value):
        self.degree = value
        self.updateAfterEveryChange()

    def changeNoChunks(self,value):
        self.noChunks = value
        self.updateAfterEveryChange()

    def updateAfterEveryChange(self):
        
        # Calc. precentage of data
        change = round(self.precentage / 100 * len(self.timePlot))

        # Select the precentage of the data
        xTimePlot = self.timePlot[:change]
        yMainDataPlot = self.mainDataPlot[:change]

        # Clear Chunks
        # self.mainPlot.set_data(yMainDataPlot, xTimePlot)
        self.mainPlot.clearChunks()
        self.chunksList.clear()
        self.chunksList.addItem("no.")
        self.latex.clear()

        precentageErrorFinal = self.calcChunks(xTimePlot,yMainDataPlot,self.noChunks,self.degree,self.overlap,true)
        # Calculate the precentage error
        self.ErrorPrecent.setText("{:.3f}%".format(precentageErrorFinal))

    def calcChunks(self, xTimePlot, yMainDataPlot, noChunks, degree, overlap, status):
        # Calc. the period of each chunk
        period = len(xTimePlot) / noChunks
        # Calc. the overlap period
        overlapPeriod = overlap/100 * period
        
        self.latexList = list()
        precentageError = list()
        start, end = 0, 0
        i = 0 # iteration
        n = 1
        while i+period-overlapPeriod <= len(xTimePlot):
            # Calculate the start and end of each chunk
            if i != 0:
                start = int(i-overlapPeriod)
                end = int(i-overlapPeriod+period)
                i += period-overlapPeriod
            else:
                start = int(i)
                end = int(i+period)
                i+=period
            
            if i+period-overlapPeriod > len(xTimePlot):
                end = len(xTimePlot)

            # Chunk Time
            chunkTime = xTimePlot[start:end]
            # Poly fit
            chunkCoeff = np.polyfit(xTimePlot[start:end], yMainDataPlot[start:end], degree)
            latexChunk = np.poly1d(chunkCoeff)

            if status == True:
                # Convert from poly to latex in string form
                latexString = self.generateLatexString(latexChunk)
                self.latexList.append(latexString)
                self.chunksList.addItem(str(n))
                
                n+=1

            # Calc. the curve from equation of latex
            chunkData = np.zeros(int(end-start)) # Initilize the chunkData
            for j in range(int(end-start)):
                chunkData[j] = latexChunk(chunkTime[j])
            
            chunkError = self.MeanAbsoluteError(yMainDataPlot[start:end],chunkData)
            precentageError.append(chunkError)

            if status == True:
                self.mainPlot.plotChunks(chunkTime, chunkData)

        # Calculate the precentage error
        precentageErrorFinal = np.mean(precentageError)

        return precentageErrorFinal

    def MeanAbsoluteError(self,y_true, y_chunk):
            y_true, y_chunk = np.array(y_true), np.array(y_chunk)
            return ((np.mean(np.abs(y_true - y_chunk))/(np.abs(np.mean(y_true))))*100)

    def generateLatexString(self, latexPoly):
        coeff = latexPoly.c
        latexString = "$"
        for i in range(latexPoly.order,-1,-1) :
            coeff = latexPoly.c
            if i == 0:
                latexString += "{:.3f}".format(coeff[0])
            elif i == 1:
                latexString += "{:.2f}X".format(coeff[1])
            else:
                latexString += "{:.2f}X^{}".format(coeff[i],i)                
            
            if i != 0 :
                latexString += "+"
        
            i+=1
        latexString += "$"

        return latexString

    def latexToLabel(self, mathTex, fs):
        #---- set up a mpl figure instance ----

        fig = Figure()
        fig.patch.set_facecolor('none')
        fig.set_canvas(FigureCanvasAgg(fig))
        renderer = fig.canvas.get_renderer()

        #---- plot the mathTex expression ----

        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.patch.set_facecolor('none')
        t = ax.text(0, 0, mathTex, ha='left', va='bottom', fontsize=fs)

        #---- fit figure size to text artist ----

        fwidth, fheight = fig.get_size_inches()
        fig_bbox = fig.get_window_extent(renderer)

        text_bbox = t.get_window_extent(renderer)

        tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
        tight_fheight = text_bbox.height * fheight / fig_bbox.height

        fig.set_size_inches(tight_fwidth, tight_fheight)

        #---- convert mpl figure to QPixmap ----

        buf, size = fig.canvas.print_to_buffer()
        qimage = QImage.rgbSwapped(QImage(buf, size[0], size[1],
                                                    QImage.Format_ARGB32))
        qpixmap = QPixmap(qimage)

        # latexLabel = QLabel()
        # latexLabel.setPixmap(qpixmap)

        return qpixmap

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
            
            self.mainPlot.clearSignal()
            self.mainPlot.set_data(self.mainDataPlot, self.timePlot)
            self.mainPlot.plotSignal()
        
        except:
            logging.error("Can't open a csv file")

    # TODO: X AND Y in one function (self, "x or y", value)
    def yAxisChange(self, value):
        self.yErrorMap = value  
        self.errorMapPlot.setAxesLabel("y", value)

    def xAxisChange(self, value):
        self.xErrorMap = value
        self.errorMapPlot.setAxesLabel("x", value)

    def generateErrorMap(self):
        xRange = 0
        yRange = 0

        if self.yErrorMap == self.xErrorMap:
            logging.error('The user chose the same for the x and y Axis') 
            QMessageBox.information(self , "Error" , "Choose different axis for x and y.")
            return
        
        if self.yErrorMap == "":
            logging.error('Not chosen y axis') 
            QMessageBox.information(self , "Error" , "Choose the y axis!")
            return
        
        if self.xErrorMap == "":
            logging.error('Not chosen x axis') 
            QMessageBox.information(self , "Error" , "Choose the x axis!")
            return
        
        if self.xErrorMap == "Overlap":
            xRange = 25
        elif self.xErrorMap == "Degree":
            xRange = 8
        elif self.xErrorMap == "No. of Chunks":
            xRange = int(len(self.timePlot)/100)
        
        if self.yErrorMap == "Overlap":
            yRange = 25
        elif self.yErrorMap == "Degree":
            yRange = 8
        elif self.yErrorMap == "No. of Chunks":
            yRange = int(len(self.timePlot)/10)

        self.ButtonProgressBar.setText("Cencel")
        
        errorData = np.zeros((xRange,yRange))
        for x in range(1,xRange-1):
            for y in range(1,yRange-1):                
                    errorData[x][y] = self.calcChunks(self.timePlot,self.mainDataPlot, x, y, 0, False)

        self.errorMapPlot.set_data_channel(errorData)
        self.errorMapPlot.plotErrorMap()
    
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

