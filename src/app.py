# !/usr/bin/python

# AdditionsQt
from cProfile import label
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

        # Initialize Variable
        self.mainDataPlot = np.array([])
        self.timePlot = np.array([])

        self.overlap = 0
        self.precentage = 100
        self.noChunks = 0
        self.efficiency = 0
        self.degree = 0
        
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
        self.efficiencyBox.valueChanged.connect(lambda: self.changeEfficiency(self.efficiencyBox.value()))
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
        self.noChunksBox.valueChanged.connect(lambda: self.changeNoChunks(self.noChunksBox.value()))
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
        self.degreeBox.valueChanged.connect(lambda: self.changeDegree(self.degreeBox.value()))
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
        self.overlapBox.valueChanged.connect(lambda: self.changeOverLap(self.overlapBox.value()))
        overlapLayout.addWidget(overlapLabel,1)
        overlapLayout.addWidget(self.overlapBox,5)

        # Overlap Text Box
        precentageLayout = QVBoxLayout()
        precentageLabel = QLabel("Data precentage %")
        sliderLayout = QHBoxLayout()
        self.precentageSlider = QSlider(Qt.Horizontal)
        self.precentageSlider.setMinimum(0)
        self.precentageSlider.setMaximum(100)
        self.precentageSlider.setValue(100)
        self.precentageSlider.valueChanged.connect(lambda: self.changePrecentage(self.precentageSlider.value()))
        self.precentageCount = QLabel("100%")
        # self.precentageSlider.setStyleSheet(f"""font-size:14px; 
        #                     padding: 5px 15px; 
        #                     background: {COLOR4};
        #                     color: {COLOR1};""")
        sliderLayout.addWidget(self.precentageSlider,10)
        sliderLayout.addWidget(self.precentageCount,1)

        overlapLayout.addWidget(precentageLabel,1)
        overlapLayout.addLayout(sliderLayout,5)

        mainPanel.addLayout(efficiencyLayout)
        mainPanel.addLayout(noChunksLayout)
        mainPanel.addLayout(degreeLayout)
        mainPanel.addLayout(overlapLayout)
        mainPanel.addLayout(precentageLayout)

        # Main Plot
        plotLayout = QVBoxLayout()
        
        self.latex = QLabel("")
        self.latex.setStyleSheet("padding:5px; font-size:25px;")

        self.mainPlot = MplCanvasPlotter("Main Plot")
        plotLayout.addWidget(self.latex ,1)
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
        
        
        yAxisLayout.addWidget(yAxisOverLap)
        yAxisLayout.addWidget(yAxisDegree)
        yAxisLayout.addWidget(yAxisChunks)

        mapPanelLayout.addWidget(xAxisGroupBox)
        mapPanelLayout.addWidget(yAxisGroupBox)

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

    def changeEfficiency(self,value):
        self.efficiency = value
        self.updateAfterEveryChange()

    def updateAfterEveryChange(self):
        change = round(self.precentage / 100 * len(self.timePlot))

        xTimePlot = self.timePlot[:change]
        yMainDataPlot = self.mainDataPlot[:change]

        period = int(len(xTimePlot) / self.noChunks)

        i = 0
        while i+period < len(xTimePlot):
            chunkTime = xTimePlot[i:i+period]
            chunkCoeff = np.polyfit(xTimePlot[i:i+period],yMainDataPlot[i:i+period], self.degree)
            latexChunk = np.poly1d(chunkCoeff)
            # Convert from poly to latex in string form
            latexString = self.generateLatexString(latexChunk)
            # Update label
            try:
                latexPixmap = self.latexToLabel(latexString,15)
                # Update latex text
                self.latex.setPixmap(latexPixmap)
            except: 
                pass

            # Calc. the curve from equation of latex
            chunkData = np.zeros(len(chunkTime)) # Initilize the chunkData
            for j in range(len(chunkCoeff)):
                chunkData += latexChunk(j) * np.array(np.power(chunkTime,j))
            
            self.mainPlot.plotChunks(chunkTime, chunkData)
            i+= period

    def generateLatexString(self, latexPoly):
        coeff = latexPoly.c
        latexString = "$Eq.= "
        print(latexPoly.order)
        i = 0
        while i <= latexPoly.order :
            coeff = latexPoly.c
            if i == 0:
                latexString += "{:.2f}".format(coeff[i])
            elif i == 1:
                latexString += "{:.2f}x".format(coeff[i])
            else:
                latexString += "{:.2f}x^{}".format(coeff[i],i)                
            
            if i == latexPoly.order-1 :
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
        self.yAxisLabel.setText(value)

    def xAxisChange(self, value):
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

