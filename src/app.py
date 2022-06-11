# !/usr/bin/python

# AdditionsQt
from functools import partial
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
from scipy.stats import pearsonr
from scipy.interpolate import splev, splrep, interp1d


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
        self.thread = QThread()
        self.worker = ErrorMapWorker()

        self.mainDataPlot = np.array([])
        self.timePlot = np.array([])
        
        # interpolation variables
        self.overlap = 0
        self.precentage = 100
        self.noChunks = 1
        self.degree = 0
        self.latexList = list()

        # extrapolation variables
        self.extraPolyMode = False
        
        # spline variables
        self.noSamples = 1
        self.degreeSpline = 1

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
        
        panelGroupBox = QGroupBox("Interpolation Panel")
        mainPanel = QVBoxLayout()
        panelGroupBox.setLayout(mainPanel)

        tabs = QTabWidget()
        tabs.setStyleSheet(f"""font-size:15px;""")

        # TODO: Add tabs and its functions
        self.polyTab = QWidget()
        self.polyLayout()
        tabs.addTab(self.polyTab, "Polynomial")

        self.splineTab = QWidget()
        self.splineLayout()
        tabs.addTab(self.splineTab, "Spline")

        self.nearestTab = QWidget()
        self.nearestLayout()
        tabs.addTab(self.nearestTab, "Nearest")

        mainPanel.addWidget(tabs)

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

        # Color palette
        colorMapGroupBox = QGroupBox("Cmap")
        colorMapAxisLayout = QHBoxLayout()
        colorMapGroupBox.setLayout(colorMapAxisLayout)

        self.cmapList = QComboBox()
        self.cmapList.addItem("viridis")
        self.cmapList.addItem("plasma")
        self.cmapList.addItem("inferno")
        self.cmapList.addItem("magma")
        self.cmapList.addItem("rainbow") 

        mapPanelLayout.addWidget(xAxisGroupBox)
        mapPanelLayout.addWidget(yAxisGroupBox)
        mapPanelLayout.addWidget(self.cmapList)

        # Error Map Plot
        leftLayout = QVBoxLayout()
        
        self.ErrorPrecent = QLineEdit("%")
        self.ErrorPrecent.setStyleSheet("padding:3px; font-size:15px;")
        self.ErrorPrecent.setDisabled(True)

        self.errorMapPlot = MplCanvasErrorMap("Error Map")
        
        progressLayout = QHBoxLayout()
        self.progressbar = QProgressBar(self, minimum=0, maximum=100, objectName="RedProgressBar")
        self.ButtonProgressBar = QPushButton("Start")
        self.ButtonProgressBar.setStyleSheet("padding:2px; font-size:15px;")
        self.cancelButtonProgressBar = QPushButton("Cancel")
        self.cancelButtonProgressBar.setStyleSheet("padding:2px; font-size:15px;")
        self.cancelButtonProgressBar.hide()

        progressLayout.addWidget(self.progressbar,10)
        progressLayout.addWidget(self.ButtonProgressBar,2)
        progressLayout.addWidget(self.cancelButtonProgressBar,2)

        leftLayout.addWidget(self.ErrorPrecent)
        leftLayout.addWidget(self.errorMapPlot)
        leftLayout.addLayout(progressLayout)
        
        mapLayout.addWidget(mapGroupBox, 3)
        mapLayout.addLayout(leftLayout ,7)

        outerLayout.addLayout(mainLayout)
        outerLayout.addLayout(mapLayout)
        ######### INIT GUI #########

        centralMainWindow.setLayout(outerLayout)

    def polyLayout(self):
        polyLayout = QVBoxLayout()

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
        self.degreeBox.setMinimum(0)
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
        self.precentageSlider.setMinimum(1)
        self.precentageSlider.setMaximum(100)
        self.precentageSlider.setValue(100)
        
        self.precentageCount = QLabel("100%")
        sliderLayout.addWidget(self.precentageSlider,10)
        sliderLayout.addWidget(self.precentageCount,1)

        precentageLayout.addWidget(precentageLabel,1)
        precentageLayout.addLayout(sliderLayout,5)
        
        polyLayout.addLayout(noChunksLayout)
        polyLayout.addLayout(degreeLayout)
        polyLayout.addLayout(overlapLayout)
        polyLayout.addLayout(precentageLayout)

        self.polyTab.setLayout(polyLayout)

    def splineLayout(self):
        splineLayout = QVBoxLayout()

        # Num. of chunks Text Box
        noSamplesLayout = QVBoxLayout()
        noSamplesLabel = QLabel("Num. of samples")
        self.noSamplesBox = QSpinBox(self)
        self.noSamplesBox.setMinimum(1)
        self.noSamplesBox.setStyleSheet(f"""font-size:14px; 
                                padding: 5px 15px; 
                                background: {COLOR4};
                                color: {COLOR1};""")
        noSamplesLayout.addWidget(noSamplesLabel,1)
        noSamplesLayout.addWidget(self.noSamplesBox,5)

        # Polynomial Degree Text Box
        degreeLayout = QVBoxLayout()
        degreeLabel = QLabel("Degree of the spline")
        self.degreeSplineBox = QSpinBox(self)
        self.degreeSplineBox.setMinimum(1)
        self.degreeSplineBox.setMaximum(5)
        self.degreeSplineBox.setStyleSheet(f"""font-size:14px; 
                            padding: 5px 15px; 
                            background: {COLOR4};
                            color: {COLOR1};""")
        degreeLayout.addWidget(degreeLabel,1)
        degreeLayout.addWidget(self.degreeSplineBox,5)

        splineLayout.addLayout(noSamplesLayout)
        splineLayout.addLayout(degreeLayout)
        splineLayout.addSpacerItem(QSpacerItem(10,100,QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.splineTab.setLayout(splineLayout)

    def nearestLayout(self):
        nearestLayout = QVBoxLayout()
        
        # Num. of chunks Text Box
        noSamplesNearestLayout = QVBoxLayout()
        noSamplesNearestLabel = QLabel("Num. of samples")
        self.noSamplesNearestBox = QSpinBox(self)
        self.noSamplesNearestBox.setMinimum(2)
        self.noSamplesNearestBox.setStyleSheet(f"""font-size:14px; 
                                padding: 5px 15px; 
                                background: {COLOR4};
                                color: {COLOR1};""")
        noSamplesNearestLayout.addWidget(noSamplesNearestLabel,1)
        noSamplesNearestLayout.addWidget(self.noSamplesNearestBox,5)
        
        nearestLayout.addLayout(noSamplesNearestLayout)
        nearestLayout.addSpacerItem(QSpacerItem(10,200,QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.nearestTab.setLayout(nearestLayout)

    # Connect actions
    def connect(self):
        self.chunksList.currentTextChanged.connect(lambda: self.chunkLatexChange(self.chunksList.currentText()))

        self.noChunksBox.valueChanged.connect(lambda: self.changeNoChunks(self.noChunksBox.value()))
        self.overlapBox.valueChanged.connect(lambda: self.changeOverLap(self.overlapBox.value()))
        self.precentageSlider.valueChanged.connect(lambda: self.changePrecentage(self.precentageSlider.value()))
        self.degreeBox.valueChanged.connect(lambda: self.changeDegree(self.degreeBox.value()))

        self.noSamplesBox.valueChanged.connect(lambda: self.changeNoSamples(self.noSamplesBox.value()))
        self.degreeSplineBox.valueChanged.connect(lambda: self.changeDegreeSpline(self.degreeSplineBox.value()))

        self.noSamplesNearestBox.valueChanged.connect(lambda: self.changeNoSamplesNearest(self.noSamplesNearestBox.value()))

        # Error map
        self.ButtonProgressBar.clicked.connect(lambda: self.generateErrorMap())
        self.cancelButtonProgressBar.clicked.connect(lambda: self.worker.stop())

        self.xAxisOverLap.clicked.connect(lambda: self.xAxisChange(self.xAxisOverLap.text()))
        self.xAxisDegree.clicked.connect(lambda: self.xAxisChange(self.xAxisDegree.text()))
        self.xAxisChunks.clicked.connect(lambda: self.xAxisChange(self.xAxisChunks.text()))

        self.yAxisOverLap.clicked.connect(lambda: self.yAxisChange(self.yAxisOverLap.text()))
        self.yAxisDegree.clicked.connect(lambda: self.yAxisChange(self.yAxisDegree.text()))
        self.yAxisChunks.clicked.connect(lambda: self.yAxisChange(self.yAxisChunks.text()))

        self.cmapList.currentTextChanged.connect(self.colorErrorMapChange)

    def colorErrorMapChange(self, color):
        self.statusBar.showMessage("Spectrogram platte color is changed to " + color + ".")
        self.errorMapPlot.set_color(color)
    
    def chunkLatexChange(self, i):
        # Update label
        try:
            latexPixmap = self.latexToLabel(self.latexList[int(i)-1], 13)
            # Update latex text
            self.latex.setPixmap(latexPixmap)
        except: 
            pass
    
    # Nearest
    def changeNoSamplesNearest(self,value):
        self.noSamplesNearest = value - 1
        self.updateAfterEveryChangeNearest()
 
    def updateAfterEveryChangeNearest(self):     
        if len(self.timePlot) > 0:     

            if self.noSamplesNearest >= 2:
                self.mainPlot.plotSignalOnly()
                self.chunksList.clear()
                self.chunksList.addItem("no.")
                self.latex.clear()

                xi = self.timePlot[::int(len(self.mainDataPlot)/(self.noSamplesNearest))]
                yi = self.mainDataPlot[::int(len(self.mainDataPlot)/(self.noSamplesNearest))]

                interp = interp1d(xi, yi, kind="nearest", fill_value="extrapolate")
                y_nearest = interp(self.timePlot)

                self.mainPlot.plotSpline(xi, yi, self.timePlot, y_nearest)

                precentageErrorFinal = self.meanAbsoluteError(self.mainDataPlot, y_nearest)
                self.ErrorPrecent.setText("{:.3f}%".format(precentageErrorFinal))

            else:
                QMessageBox.critical(self, "Error", "Choose No. of samples bigger than 2.")

        else:
            QMessageBox.critical(self, "Error", "You must open a signal.")

    # Spline
    def changeNoSamples(self,value):
        self.noSamples = value-1
        self.updateAfterEveryChangeSpline()
    
    def changeDegreeSpline(self,value):
        self.degreeSpline = value
        self.updateAfterEveryChangeSpline()
    
    def updateAfterEveryChangeSpline(self):
        if len(self.timePlot) > 0:
            if self.noSamples>self.degreeSpline:
                self.mainPlot.plotSignalOnly()
                self.chunksList.clear()
                self.chunksList.addItem("no.")
                self.latex.clear()

                x = self.timePlot[::int(len(self.mainDataPlot)/(self.noSamples))]
                y = self.mainDataPlot[::int(len(self.mainDataPlot)/(self.noSamples))]
                spl = splrep(x, y, k=self.degreeSpline)
                y2 = splev(self.timePlot, spl)

                precentageErrorFinal = self.meanAbsoluteError(self.mainDataPlot, y2)
                self.ErrorPrecent.setText("{:.3f}%".format(precentageErrorFinal))

                self.mainPlot.plotSpline(x, y, self.timePlot, y2)
            else:
                QMessageBox.critical(self, "Error", "No. of samples > the degree of the spline fit must hold.")
        else:
            QMessageBox.critical(self, "Error", "You must open a signal.")

    # Polynomial
    def changePrecentage(self,value):
        self.precentageCount.setText(str(value)+'%')
        self.precentage = value
        self.updateAfterEveryChangePoly()
    
    def changeOverLap(self,value):
        self.overlap = value
        self.updateAfterEveryChangePoly()
    
    def changeDegree(self,value):
        self.degree = value
        self.updateAfterEveryChangePoly()

    def changeNoChunks(self,value):
        self.noChunks = value
        self.updateAfterEveryChangePoly()

    def updateAfterEveryChangePoly(self):
        
        if len(self.timePlot) > 0:
            # Calc. precentage of data
            change = round(self.precentage / 100 * len(self.timePlot))

            # Select the precentage of the data
            xTimePlot = self.timePlot[:change]
            yMainDataPlot = self.mainDataPlot[:change]

            # Clear Chunks
            self.mainPlot.plotSignalOnly()
            self.chunksList.clear()
            self.chunksList.addItem("no.")
            self.latex.clear()

            if self.precentage == 100 :
                self.noChunksBox.setDisabled(False)
                self.extraPolyMode == False
                self.degreeBox.setMaximum(8)

                # TODO: prevent repeation code
                precentageErrorFinal = self.calcChunks(xTimePlot,yMainDataPlot,self.noChunks,self.degree,self.overlap)
            else :
                if self.extraPolyMode == False:
                    QMessageBox.information(self , "Extrapolation" , "You are in extrapolation mode now.")
                
                self.extraPolyMode = True
                self.noChunksBox.setValue(1)
                self.degreeBox.setMaximum(100)
                self.noChunksBox.setDisabled(True)
                precentageErrorFinal = self.calcChunks(xTimePlot, yMainDataPlot, self.noChunks,self.degree,self.overlap)
                self.calcExtrapolation(self.degree, change-1)

            # Calculate the precentage error
            self.ErrorPrecent.setText("{:.3f}%".format(precentageErrorFinal))
        else:
            QMessageBox.critical(self, "Error", "You must open a signal.")

    def calcChunks(self, xTimePlot, yMainDataPlot, noChunks, degree, overlap):

        # Calc. the period of each chunk
        period = len(xTimePlot) / noChunks
        # Calc. the overlap period
        overlapPeriod = overlap/100 * period
        
        prevOverlapChunkData = list()
        currOverlapChunkData = list()        
        chunkError = list()
        
        self.latexList = list()
        precentageError = list()
        start, end = 0, 0
        i = 0 # iteration
        n = 1
        
        while i+period-overlapPeriod <= len(xTimePlot):
            # Calculate the start and end of each chunk
            if i != 0:
                start = int(i-overlapPeriod)
                end = int(i-(overlapPeriod)+period)
                i += period-overlapPeriod
            else:
                start = int(i)
                end = int(i+period)
                i+=period
                startOverlap = int(i-overlapPeriod)
                endoverlap = int(i)
            
            if i+period-overlapPeriod > len(xTimePlot):
                end = len(xTimePlot)

            # Chunk Time
            chunkTime = xTimePlot[start:end]
            # Poly fit
            chunkCoeff = np.polyfit(xTimePlot[start:end], yMainDataPlot[start:end], degree)
            latexChunk = np.poly1d(chunkCoeff)

            # Convert from poly to latex in string form
            latexString = self.generateLatexString(latexChunk)
            self.latexList.append(latexString)
            self.chunksList.addItem(str(n))

            # Calc. the curve from equation of latex
            chunkData = np.zeros(int(end-start)) # Initilize the chunkData
            for j in range(int(end-start)):
                chunkData[j] = latexChunk(chunkTime[j])

            if overlap != 0 :
                if n == 1:
                    prevOverlapChunkData = chunkData[startOverlap:endoverlap] # Get last overlap period
                else:
                    currOverlapChunkData = chunkData[:int(overlapPeriod)] # Get first overlap period
                                        
                    if len(prevOverlapChunkData) != len(currOverlapChunkData):
                        currOverlapChunkData = np.append(currOverlapChunkData,currOverlapChunkData[-1])
                    
                    prevOverlapChunkData = chunkData[startOverlap:endoverlap] # Get last overlap period
                    chunkOverlap = np.mean([prevOverlapChunkData,currOverlapChunkData], axis=0)
                    
                    try:
                        chunkData[:int(overlapPeriod)] = chunkOverlap
                    except:
                        chunkData[:int(overlapPeriod)] = chunkOverlap[:-1]

                if end != len(xTimePlot):
                    chunkData = chunkData[:-int(overlapPeriod)]
                    chunkTime = chunkTime[:-int(overlapPeriod)]
          
            self.mainPlot.plotChunks(chunkTime, chunkData)

            if end != len(xTimePlot):
                chunkError = self.meanAbsoluteError(yMainDataPlot[start:end-int(overlapPeriod)],chunkData)

            precentageError.append(chunkError)
            n+=1

        # Calculate the precentage error
        precentageErrorFinal = np.mean(precentageError)
        return precentageErrorFinal

    def calcExtrapolation(self, degree, change):
        # Chunk Time
        chunkTime = self.timePlot[change:]
        # Poly fit
        chunkCoeff = np.polyfit(self.timePlot[:change], self.mainDataPlot[:change], degree)
        latexChunk = np.poly1d(chunkCoeff)

        # Calc. the curve from equation of latex
        chunkData = np.zeros(len(chunkTime)) # Initilize the chunkData
        for j in range(len(chunkTime)):
            chunkData[j] = latexChunk(chunkTime[j])

        chunkData = np.append(latexChunk(self.timePlot[change-1]), chunkData)
        xTimePlot = np.append(chunkTime, chunkTime[-1] + chunkTime[-2]-chunkTime[-3])
        self.mainPlot.plotChunks(xTimePlot, chunkData)

        return

    def meanAbsoluteError(self, y_true, y_chunk):
            y_true, y_chunk = np.array(y_true), np.array(y_chunk)
            corr, _ = pearsonr(y_true, y_chunk)
            return (1-corr)*100

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
                return
                    
            if fileExtension == "csv(*.csv)":

                if (len(pd.read_csv(path).iloc[:,1].values.tolist()) <= 500):
                    QMessageBox.critical(self, "Error", "You must choose a signal with a reasonable length near of 1000 points.")
                    return

                if (len(self.timePlot) > 5000 and len(self.timePlot) < 12500):
                        self.mainDataPlot = pd.read_csv(path).iloc[::10,1].values.tolist()
                        self.timePlot = pd.read_csv(path).iloc[::10,0].values.tolist()
                else:
                    self.mainDataPlot = pd.read_csv(path).iloc[:,1].values.tolist()
                    self.timePlot = pd.read_csv(path).iloc[:,0].values.tolist()
            
            self.mainPlot.clearSignal()
            self.mainPlot.set_data(self.mainDataPlot, self.timePlot)
            self.mainPlot.plotSignal()
            self.noSamplesBox.setMaximum(int(len(self.mainDataPlot)/2))
        
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
        
        if(len(self.timePlot) > 10):
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = ErrorMapWorker()

            if self.yErrorMap == self.xErrorMap:
                logging.error('The user chose the same for the x and y Axis') 
                QMessageBox.critical(self , "Error" , "Choose different axis for x and y.")
                return
            
            if self.yErrorMap == "":
                logging.error('Not chosen y axis') 
                QMessageBox.critical(self , "Error" , "Choose the y axis!")
                return
            
            if self.xErrorMap == "":
                logging.error('Not chosen x axis') 
                QMessageBox.critical(self , "Error" , "Choose the x axis!")
                return

            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)

            # Step 5: Connect signals and slots
            self.thread.started.connect(partial(self.worker.run,self.timePlot, self.mainDataPlot, self.xErrorMap, self.yErrorMap))
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.reportProgress)
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.ButtonProgressBar.hide()
            self.cancelButtonProgressBar.show()

            self.worker.errorsData.connect(self.errorMapPlot.set_data_channel)
            self.thread.finished.connect(
                lambda: self.ButtonProgressBar.show()
            )
            self.thread.finished.connect(
                lambda: self.cancelButtonProgressBar.hide()
            )
            self.thread.finished.connect(
                lambda: self.errorMapPlot.plotErrorMap()
            )

            self.thread.finished.connect(
                lambda: self.progressbar.setValue(0)
            )
        else:
            QMessageBox.critical(self, "Error", "You must open a signal.")

    def reportProgress(self, n):
        self.progressbar.setValue(n)
    
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