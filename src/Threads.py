# importing Qt widgets
from PyQt5.QtCore import QObject, pyqtSignal

from scipy.stats import pearsonr # Correlation 
import numpy as np

import warnings
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
    finishedCalc = pyqtSignal()
    precentageErrorVar = pyqtSignal(int)
    
    def __init__(self):
        super(ErrorMapWorker, self).__init__()
        self._isRunning = True

    def run(self, timePlot, mainDataPlot, xErrorMap, yErrorMap): 
        if not self._isRunning :
            self._isRunning = True

        xRange = self.getRanges(xErrorMap,timePlot)
        yRange = self.getRanges(yErrorMap,timePlot)

        i = 1
        errorsData = list()
        for y in range(1,yRange):
            tempErrors = np.array([])
            for x in range(1,xRange):
                if self._isRunning :             
                    errorData = self.chosenAxis(timePlot, mainDataPlot, xErrorMap, yErrorMap, x, y)
                    tempErrors = np.append(tempErrors, errorData)
                    # Return progress bar
                    self.progress.emit(int(i/((xRange-1)*(yRange-1))*100))
                    i += 1
            errorsData.append(tempErrors)

        errorsData = np.array(errorsData)
        if self._isRunning :
            self.errorsData.emit(errorsData[::-1])
        
        self.finished.emit()

    def getRanges(self, axisErrorMap,timePlot):
        axisRange = 0

        if axisErrorMap == "Overlap":
            axisRange = 10
        elif axisErrorMap == "Degree":
            axisRange = 5
        elif axisErrorMap == "No. of Chunks":
            axisRange = int(len(timePlot)/10)
        
        return axisRange

    def chosenAxis(self, timePlot, mainDataPlot, xErrorMap, yErrorMap, x, y):
        errorData = 0
        if xErrorMap == "Overlap" and yErrorMap == "Degree":
            errorData = self.calcChunks(timePlot, mainDataPlot, 5, y, x)
        elif xErrorMap == "Overlap" and yErrorMap == "No. of Chunks":
            errorData = self.calcChunks(timePlot, mainDataPlot, y, 1, x)
        elif xErrorMap == "Degree" and yErrorMap == "Overlap":
            errorData = self.calcChunks(timePlot, mainDataPlot, 5, x, y)
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

            if end != len(xTimePlot):
                chunkError = self.meanAbsoluteError(yMainDataPlot[start:end], chunkData)
            
            precentageError.append(chunkError)

            n+=1
        
        # Calculate the precentage error
        precentageErrorFinal = np.mean(precentageError)
        return precentageErrorFinal

    def calcChunksRun(self, xTimePlot, yMainDataPlot, noChunks, degree, overlap):
        self.precentageErrorVar = self.calcChunks(self, xTimePlot, yMainDataPlot, noChunks, degree, overlap)
        self.precentageErrorVar.emit()
        self.finishedCalc.emit()

    def meanAbsoluteError(self, y_true, y_chunk):

        y_true, y_chunk = np.array(y_true), np.array(y_chunk)
        corr, _ = pearsonr(y_true, y_chunk)
        return (1-corr)*100


    def stop(self):
        self._isRunning = False