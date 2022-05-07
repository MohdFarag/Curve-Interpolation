import os
from time import sleep
from scipy.stats import pearsonr

from PyQt5.QtCore import QObject, QThread, pyqtSignal
import numpy as np
# Logging configuration
import logging
logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=logging.INFO)

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

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