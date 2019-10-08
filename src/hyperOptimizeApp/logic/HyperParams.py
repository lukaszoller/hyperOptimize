import numpy as np


class HyperParams:
    """
    This class contains the following hyperparms for the optimizer to test:
    1. Learning rate: 1D matlabArray
    2. Learning rate decay: 1D matlabArray
    3. loss function: adam, mean_squared_error
    4. nbr layers: 1D matlabArray
    5 nbr of Units per Layer: 1D matlabArray
    6. dropout rate: 1D matlabArray

    1D means, that for each iteration in the optimizer loop the same nbr of units per layer and dropout rate per layer is
    used. Otherwise it had to be a 2D array / matrix with an array telling how much units per layer / dropout rate per layer
    is used for each iteration.
    """
    def __init__(self):
        self.learningRateArray = np.array()
        self.lrDecayArray = np.array()
        self.lossFunctionArray = np.array()
        self.nbrOfLayersArray = np.array()
        self.nbrOfNodesPerLayerArray = np.array()
        self.dropoutRatePerArray = np.array()
