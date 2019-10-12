from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

class EstimateTimeModel:
    def __init__(self):
        saverLoader = SaverLoader()
        (x,y) = saverLoader.getEstTimeData()
        self.x = x
        self.y = y

    def estimateTime(self, hyperParamsList):         # Code mostly from https://realpython.com/linear-regression-in-python/
        """This method trains a linear model (with polynomial features) to predict the running time of the optimization.
        The model is trained with data from earlier optimizations."""
        # Add polynomial features to training data
        transformer = PolynomialFeatures(degree=3, include_bias=True)
        xPoly = transformer.fit_transform(self.x)

        estTimeModel = LinearRegression(normalize=True).fit(xPoly, self.y)

        # Add polinomial featurs to hyperParameters
        hyperParams = self.hyperParamsListToData(hyperParamsList)
        hyperParamsPoly = transformer.fit_transform(np.array(hyperParams).reshape(1, -1))
        # predict Time
        return estTimeModel.predict(hyperParamsPoly)
        # return estTimeModel.predict(xPoly)        ## Just to check if training y are more or less like prediction

    def storeTimeMeasurements(self, hyperParamsList, timeMeasurement):
        ###########################################################
        # Get Data
        ###########################################################
        [nbrOfModels, sumOfLayers, sumOfNodes] = self.hyperParamsListToData(hyperParamsList)
        ###########################################################
        # Store data
        ###########################################################
        # Append new data
        self.x = self.x.append([nbrOfModels, sumOfLayers, sumOfNodes], axis=0)
        self.y = self.y.append(timeMeasurement)

        # Save all
        SaverLoader.saveTimeMeasurementData(self.x, self.y)


    def hyperParamsListToData(self, hyperParamsList):
        """This method converts hyperParamsList, a list of dicts where every dict stands for the
        hyperparams of one model, to 3 measurements:
        1. number of models
        2. sum of Nodes (sum of the nodes of all models)
        3. sum of layers (sum of the layers of all models)"""
        # Counts all dicts in hyperParamsList (a list of dict, for every model 1 dict)
        nbrOfModels = len(hyperParamsList)
        # Sum up nbr of Nodes and layers
        sumOfNodes = 0
        sumOfLayers = 0
        for d in hyperParamsList:
            sumOfNodes = sumOfNodes + sum(d['nodesPerLayer'])
            sumOfLayers = sumOfLayers + len(d['nodesPerLayer'])

        return nbrOfModels, sumOfNodes, sumOfLayers
