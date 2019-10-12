from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.HyperParamsDict import HyperParamsDict
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsDict import RangeForHyperParamsDict
import numpy as np
import time

class OptimizeParamsModel:
    def __init__(self, xTrain, yTrain, xTest, yTest):
        self.modelList = list()
        self.errorList = np.array()
        self.xTrain = xTrain
        self.yTrain = yTrain
        self.xTest = xTest
        self.yTest = yTest

    def estimateTime(self):
        return EstimateTimeModel.estimateTime(hyperParams=self.hyperParams)

    def createHyperParamsListRandom(self, rangeForHyperparamsDicta, nbrOfModels):
        """This method takes as input the number of models to be created and ranges for hyperparameters and returns a
        list of dicts where each dict contains the hyperparams for one model. The input object has to be a dict with the
        following names as key and as values an integer array with min, max values to specify a range OR a string array
        to specify optimizers or lossFunctions.
        Keys for this dict: numberOfLayers, numberOfNodesPerLayer, activationFunctionPerLayer,
        dropOutRatePerLayer, lossFunction, modelOptimizer, learningRate, learningRateDecay. Random: The parameter
        values will be chosen randomly from the above ranges.
        """
        rangeForHyperparamsDict = RangeForHyperParamsDict()

        #############################################################
        # Prepare arrays with values for dicts
        #############################################################

        # hiddenUnitsArray
        # 1. Choose number of layers
        nbrOfLayersMin = rangeForHyperparamsDict.nbrOfHiddenLayersDict.get('min')
        nbrOfLayersMMax = rangeForHyperparamsDict.nbrOfHiddenLayersDict.get('max')
        nbrOfLayersArray = np.random.random_integers(nbrOfLayersMin, nbrOfLayersMMax, nbrOfModels)

        # 2. Choose number of nodes per Layer
        nbrOfNodesMin = rangeForHyperparamsDict.nbrOfHiddenUnitsDict.get('min')
        nbrOfNodesMax = rangeForHyperparamsDict.nbrOfHiddenUnitsDict.get('max')
        # This results the same number of nodes per Layer for each model
        nbrOfNodesArray = np.random.random_integers(nbrOfNodesMin, nbrOfNodesMax, nbrOfModels)

        # activationArray
        indexForActivationArray = np.random.random_integers(0,len(rangeForHyperparamsDict.activationArray), nbrOfModels)
        # dropOutArray: The dropout rate for each model
        dropOutArray = np.random.random_sample(nbrOfModels)
        # lossFunction
        lossFunctionArray = np.random.choice(rangeForHyperparamsDict.lossFunctionArray, nbrOfModels, replace=False)
        # modelOptimizer
        modelOptimizerArray = np.random.choice(rangeForHyperparamsDict.modelOptimizerArray, nbrOfModels, replace=False)
        # Learning Rate (code from: https://www.coursera.org/learn/deep-neural-network/lecture/3rdqN/using-an-appropriate-scale-to-pick-hyperparameters Video: 02min55s)
        minLog = np.log10(rangeForHyperparamsDict.learningRateDict.get('min'))
        maxLog = np.log10(rangeForHyperparamsDict.learningRateDict.get('max'))
        exponents = (maxLog - minLog) * np.random.random_sample(nbrOfModels) + minLog    # see: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.random_sample.html
        learningRateArray = np.power(10, exponents)
        # learningRateDecay
        learningRateDecayArray = 4
        #############################################################
        # Construct a dict for each model with the above arrays
        #############################################################
        # Create a dict for each model
        hyperParamsList = list()

        # For loop
        for i in range(0,nbrOfModels):
            tmpNbrOfLayers = nbrOfLayersArray[i]
            # create dict
            d = HyperParamsDict()
            # Create Array with length nbrOfLayersArray[i] and all values = nbrOfNodesArray[i] <<<--- This results in the same number of nodes per Layer for each model
            d.hiddenUnitsArray = np.full(tmpNbrOfLayers, nbrOfNodesArray[i])
            d.nbrOfFeatures = rangeForHyperparamsDict.nbrOfFeatures
            d.learningRate = learningRateArray[i]
            d.modelOptimizer = modelOptimizerArray[i]
            # Choose from the range of activation functions with the above randomly created indexes the activation Function for this model
            activationFunciton = rangeForHyperparamsDict.activationArray[indexForActivationArray[i]]
            # Create Array with length nbrOfLayersArray[i] and all values = activationFunction <<<--- This results in the same activation Function per Layer for each model
            d.activationArray = np.full(tmpNbrOfLayers, rangeForHyperparamsDict.activationArray[indexForActivationArray[i]])
            # Create Array with length nbrOfLayersArray[i] and all values = dropOutRate[i] <<<--- This results in the same number of nodes per Layer for each model
            d.dropOutArray = np.full(tmpNbrOfLayers, dropOutArray[i])
            d.lossFunction = lossFunctionArray[i]
            d.learningRateDecay = learningRateDecayArray[i]
            # add dict to hyperParamsList
            hyperParamsList.append(d)
        # Return the list of dicts, each with hyperparams for each model
        return hyperParamsList

    def evaluateModels(self, hyperParamsList):
        """This method takes as input a list of dictionaries (a dict for every model to create). It creates,
        trains and evaluates models basing on this list of dictionaries and stores the time measurements for later
        time predictions. """
        # Initialize model list

        # Initialize results table (len(hyperparams(1)*len(hyperparamy(2)*...)

        # Loop through list with dictionaries with hyperparams for each model
        startTime = time.clock()
        for hyperDict in hyperParamsList:
            #####################################################################################
            # create model
            #####################################################################################
            model = MachineLearningModel()
            model.createNetwork(hyperParamsList['nbrOfFeatures'],hyperParamsList['unitsArray'],hyperParamsList['activationArray'],
                                hyperParamsList['dropOutArray'],hyperParamsList['lossFunction'],hyperParamsList['modelOptimizer'],
                                hyperParamsList['learningRate'],hyperParamsList['decay'])
            #####################################################################################
            # Train and evaluate model
            #####################################################################################
            # train model
            # last parameter = batch size
            model.trainNetwork(self.xTrain, self.y_train)

            #####################################################################################
            # Predict with test data
            #####################################################################################
            # predict data
            y_predict = model.predict(self.xTest)
            y_PredictOneCol = np.argmax(y_predict, axis=1)
            y_TestOneCol = np.argmax(self.yTest, axis=1)

            comparisonArray = y_PredictOneCol != y_TestOneCol
            errorSum = np.sum(comparisonArray)

            #####################################################################################
            # Store data from this loop
            #####################################################################################
            # store model
            self.modelList.add(model)
            # store error data

        # Give running time measurements to EstimateTimeModel
        runningTime = time.clock() - startTime
        etm = EstimateTimeModel()
        etm.storeTimeMeasurements(hyperParamsList, runningTime)




