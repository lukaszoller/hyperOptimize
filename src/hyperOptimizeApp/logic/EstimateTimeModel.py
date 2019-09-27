from persistence import SaverLoader
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

class EstimateTimeModel:
    def __init__(self, hyperParams):
        saverLoader = SaverLoader()
        (x,y) = saverLoader.getEstTimeData()
        self.x = x
        self.y = y
        self.hyperParams = hyperParams

    def estimateTime(self):         # Code mostly from https://realpython.com/linear-regression-in-python/
        # Add polynomial features
        xPoly = PolynomialFeatures(degree=3, include_bias=True).fit_transform(self.x)
        estTimeModel = LinearRegression(normalize=True).fit(xPoly, self.y, )
        # predict Time
        return estTimeModel.predict(self.hyperParams.reshape(1,-1))

e = EstimateTimeModel([1,5,0.01])
print(type(e))
#print(e.estimateTime())