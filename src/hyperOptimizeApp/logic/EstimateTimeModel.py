from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
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

    def estimateTime(self, hyperParamsObjList):         # Code mostly from https://realpython.com/linear-regression-in-python/
        """This method trains a linear model (with polynomial features) to predict the running time of the optimization.
        The model is trained with data from earlier optimizations."""
        # Add polynomial features to training data
        transformer = PolynomialFeatures(degree=3, include_bias=True)
        xPoly = transformer.fit_transform(self.x)

        # Create the linear model
        estTimeModel = LinearRegression(normalize=True).fit(xPoly, self.y)

        # Add polinomial featurs to hyperParameters
        hyperParams = self.hyperParamsListToData(hyperParamsObjList)
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


    def hyperParamsListToData(self, hyperParamsObjList):
        """This method converts hyperParamsObjList, a list of hyperParamsObj where every obj stands for the
        hyperparams of one model, to a 2D Array where each row contains information of one model (columns:
        1.nbrOfLayers, 2. nbrOfNodesPerLayer, 3. learningRate).
        This 2D array can be used:
         1. to get an estimate for the running time to construct, train and evaluate the models from this list.
         2. to add the array to the training data for the time estimation."""
        # Counts all dicts in hyperParamsList (a list of dict, for every model 1 dict)
        # Initialize a list with 3 columns and len = len(hyperParamsObjList)
        hyperParamsDataList = np.zeros((len(hyperParamsObjList, 3)))
        # loop through all hyperParamsObjects
        i = 0
        for h in hyperParamsObjList:
            h = HyperParamsObj()
            # add nbr of Layers
            hyperParamsDataList[i,0] = len(h.nbrOfNodesArray)
            # add nbr of nodes per Layer
            hyperParamsDataList[i, 1] = h.nbrOfNodesArray
            # add nbr of nodes per Layer
            hyperParamsDataList[i,2] = h.learningRate


        # Old code delete if storing data of each model makes sense
        # nbrOfModels = len(hyperParamsObjList)
        # # Sum up nbr of Nodes and layers
        # sumOfNodes = 0
        # sumOfLayers = 0
        # for d in hyperParamsObjList:
        #     sumOfNodes = sumOfNodes + sum(d['nodesPerLayer'])
        #     sumOfLayers = sumOfLayers + len(d['nodesPerLayer'])

        return hyperParamsDataList
