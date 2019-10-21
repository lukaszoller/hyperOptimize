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
        The model is trained with data from earlier optimizations.
        The return value of this function is the sum of the running times of each model which has to be built basing on
        the inputted hyperParamsObjList."""

        # Add polynomial features to training data
        transformer = PolynomialFeatures(degree=3, include_bias=True)
        xPoly = transformer.fit_transform(self.x)

        # With training data: Create the linear model and normalize data
        estTimeModel = LinearRegression(normalize=True).fit(xPoly, self.y)

        # Add polynomial features to hyperParameters
        sl = SaverLoader()
        hyperParams = sl.hyperParamsListToData(hyperParamsObjList)
        hyperParamsPoly = transformer.fit_transform(np.array(hyperParams))
        # predict Time for the whole table (for all hyperParamsObj)
        predictionTable = estTimeModel.predict(hyperParamsPoly)
        # sum up prediction time of all models
        predictionTimeForAllModels = np.sum(predictionTable)
        return predictionTimeForAllModels
        # return estTimeModel.predict(xPoly)        ## Just to check if training y are more or less like prediction

