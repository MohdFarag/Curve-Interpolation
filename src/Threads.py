import os
from time import sleep
from scipy.stats import pearsonr
import warnings

from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np
warnings.simplefilter('ignore', np.RankWarning)
# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=logging.INFO)

class ErrorMapWorker(QObject):
    
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    errorsData = pyqtSignal(np.ndarray)

    def run(self, timePlot, mainDataPlot, xErrorMap, yErrorMap):
        xRange = 0
        yRange = 0

        if xErrorMap == "Overlap":
            xRange = 25
        elif xErrorMap == "Degree":
            xRange = 5
        elif xErrorMap == "No. of Chunks":
            xRange = int(len(timePlot)/20)
        
        if yErrorMap == "Overlap":
            yRange = 25
        elif yErrorMap == "Degree":
            yRange = 5
        elif yErrorMap == "No. of Chunks":
            yRange = int(len(timePlot)/20)

        i = 1
        errorsData = np.zeros((yRange,xRange))
        for y in range(1,xRange):
            for x in range(1,yRange):                
                errorsData[x][y] = self.chosenAxis(timePlot, mainDataPlot, xErrorMap, yErrorMap, x, y)
                self.progress.emit(int(i/((xRange-1)*(yRange-1))*100))
                i += 1

        self.errorsData.emit(errorsData)
        self.finished.emit()
                
    def chosenAxis(self, timePlot, mainDataPlot, xErrorMap, yErrorMap, x, y):
        errorData = 0
        if xErrorMap == "Overlap" and yErrorMap == "Degree":
            errorData = self.calcChunks(timePlot, mainDataPlot, 1, y, x)
        elif xErrorMap == "Overlap" and yErrorMap == "No. of Chunks":
            errorData = self.calcChunks(timePlot, mainDataPlot, y, 1, x)
        elif xErrorMap == "Degree" and yErrorMap == "Overlap":
            errorData = self.calcChunks(timePlot, mainDataPlot, 1, x, y)
        elif xErrorMap == "Degree" and yErrorMap == "No. of Chunks":
            errorData = self.calcChunks(timePlot, mainDataPlot, y, x, 0)
        elif xErrorMap == "No. of Chunks" and yErrorMap == "Degree":
            errorData = self.calcChunks(timePlot, mainDataPlot, x, y, 0)
        elif xErrorMap == "No. of Chunks" and yErrorMap == "Overlap":
            errorData = self.calcChunks(timePlot, mainDataPlot, x, 1, y)
        
        return errorData

    def calcChunks(self, xTimePlot, yMainDataPlot, noChunks, degree, overlap):
        
        # Calc. the period of each chunk
        period = len(xTimePlot) / noChunks
        # Calc. the overlap period
        overlapPeriod = overlap/100 * period
        
        defaultError = list()
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

            # Calc. the curve from equation of latex
            chunkData = np.zeros(int(end-start)) # Initilize the chunkData
            for j in range(int(end-start)):
                chunkData[j] = latexChunk(chunkTime[j])

            chunkError = self.MeanAbsoluteError(yMainDataPlot[start:end],chunkData)
            precentageError.append(chunkError)

        # Calculate the precentage error
        precentageErrorFinal = np.mean(precentageError)

        return precentageErrorFinal

    def MeanAbsoluteError(self, y_true, y_chunk):
            y_true, y_chunk = np.array(y_true), np.array(y_chunk)
            corr, _ = pearsonr(y_true, y_chunk)
            return (1-corr)*100