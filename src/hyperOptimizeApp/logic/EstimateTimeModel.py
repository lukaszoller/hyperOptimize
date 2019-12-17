from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import cpuinfo
import time


class EstimateTimeModel:
    def __init__(self):
        """The constructor loads already the estimate time dataset for the different functions."""
        saverLoader = FileSystemRepository()
        (x, y) = saverLoader.getEstTimeData()
        self.x = x
        self.y = y

    def estimateTime(self, hyperParamsObjList):         # Code mostly from https://realpython.com/linear-regression-in-python/
        """This method trains a linear model (with polynomial features) to predict the running time of the optimization.
        The model is trained with data from earlier optimizations.
        The return value of this function is the sum of the running times of each model which has to be built basing on
        the inputted hyperParamsObjList. Unit: hh mm ss."""

        # Add polynomial features to training data
        transformer = PolynomialFeatures(degree=3, include_bias=True)
        xPoly = transformer.fit_transform(self.x)

        # With training data: Create the linear model and normalize data
        estTimeModel = LinearRegression(normalize=True).fit(xPoly, self.y)

        # Convert hyperParamsObjList to matrix
        sl = FileSystemRepository()
        hyperParamsData = sl.hyperParamsListToData(hyperParamsObjList)
        # Add cpu speed data to hyperParamsData
        cpuSpeed = cpuinfo.get_cpu_info()['hz_actual_raw'][0]
        newLineWithCpuSpeed = np.full((len(hyperParamsData[:,0]),1), cpuSpeed)
        hyperParamsData = np.append(hyperParamsData, newLineWithCpuSpeed, axis=1)
        # Add polynomial features to hyperParameters
        hyperParamsPoly = transformer.fit_transform(np.array(hyperParamsData))
        # predict Time for the whole table (for all hyperParamsObj)
        predictionTable = estTimeModel.predict(hyperParamsPoly)
        # sum up prediction time of all models
        predictionTimeForAllModels = np.sum(predictionTable)
        stringTime = time.strftime('%H:%M:%S', time.gmtime(predictionTimeForAllModels))
        return stringTime, predictionTimeForAllModels
        # return estTimeModel.predict(xPoly)        ## Just to check if training y are more or less like prediction

    def getEstimateTimeAccuracy(self, nbrOfValuesForMean):
        """Returns an accuracy value for self.estimateTime.
        The computation of the accuracy is just the mean of the accuracy of the last X actual accuracies where X has to
        be inputted in the function."""
        sl = FileSystemRepository()
        accuracyList = sl.estimateTimeAccuracyList
        # If nbr of accuracy measurements is smaller than nbrOfValuesForMean, just get the mean of all the measurements
        if len(accuracyList)<nbrOfValuesForMean:
            return sum(accuracyList)/len(accuracyList)
        return sum(accuracyList[-nbrOfValuesForMean:])/nbrOfValuesForMean


    def getEstimateNbrOfModels(self, availableTime):
        """Tells how many models can approximately be fittet for a given time. The approximation is just time over mean
        of models fitted so far."""

        # Get mean of model running time
        meanModelRunningTime = sum(self.y)/len(self.y)

        # return nbr of models which can be trained in availableTime
        return np.round(availableTime/meanModelRunningTime)
