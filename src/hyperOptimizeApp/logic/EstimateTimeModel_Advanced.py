from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader
import numpy as np
import statsmodels.api as sm

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

class EstimateTimeModel_Advanced:
    def __init__(self):
        saverLoader = SaverLoader()
        (x,y) = saverLoader.getEstTimeData()
        self.x = x
        self.y = y

    def estimateTime(self, hyperParams):         # Code mostly from https://realpython.com/linear-regression-in-python/
        sm.add_constant(self.x)
        model = sm.OLS(self.y, self.x)
        print(model)
        results = model.fit()
        print(results.summary())
        x_new = sm.add_constant(np.array(hyperParams).reshape(1, -1))
        print(x_new)
        return results.predict(x_new)
