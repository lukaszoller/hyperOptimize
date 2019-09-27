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

    def estimateTime(self, hyperParams):         # Code mostly from https://realpython.com/linear-regression-in-python/
        """This method trains a linear model (with polynomial features) to predict the running time of the optimization.
        The model is trained with data from earlier optimizations."""
        # Add polynomial features to training data
        transformer = PolynomialFeatures(degree=3, include_bias=True)
        xPoly = transformer.fit_transform(self.x)
        estTimeModel = LinearRegression(normalize=True).fit(xPoly, self.y)
        # Add polinomial featurs to hyperParameters
        hyperParamsPoly = transformer.fit_transform(np.array(hyperParams).reshape(1, -1))
        # predict Time
        return estTimeModel.predict(hyperParamsPoly)
        # return estTimeModel.predict(xPoly)        ## Just to check if training y are more or less like prediction

