import numpy as np
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj


class RangeForHyperParamsObj:

    MAX_NUMBER_OF_HIDDEN_LAYERS = 100

    def __init__(self):
        self.nbrOfFeatures = 0                                      #abgeleitet von Datensatz
        self.nbrOfHiddenLayersDict = dict({'min': 0, 'max': 0})     #wichtig
        self.nbrOfHiddenUnitsDict = dict({'min': 0, 'max': 0})      #wichtig von Nodes abgeleitet (Nodes pro Layer)
        self.activationArray = 0 #= np.array()                      #mal noch nicht
        self.dropOutDict = 0#= np.array()                           #irgendwas zwischen 0 und 1
        self.lossFunctionArray = 0  #= np.array()                   #verschiedene auswahlen
        self.modelOptimizerArray = 0 #= np.array()                  #
        self.learningRateDict = dict({'lrMin': 0, 'lrMax': 0})
        self.learningRateLogBool = True
        self.learningRateDecayDict = dict({'lrMin': 0, 'lrMax': 0})
        self.nbrOfCategories = 0


def createHyperParamsListRandom(rangeForHyperparamsObj, nbrOfModels):
    """This method takes as input the number of models to be created and a RangeForHyperParamsObj and returns a
    list of dicts where each dict contains the hyperparams for one model (If list has only one element it returns
    this element. The input object has to be a dict with the following names as key and as values an integer array
    with min, max values to specify a range OR a string array
    to specify optimizers or lossFunctions.
    Keys for this dict: numberOfLayers, numberOfNodesPerLayer, activationFunctionPerLayer,
    dropOutRatePerLayer, lossFunction, modelOptimizer, learningRate, learningRateDecay. Random: The parameter
    values will be chosen randomly from the above ranges.
    """

    #############################################################
    # Prepare arrays with values for dicts
    #############################################################

    # 1. Choose number of layers
    nbrOfLayersMin = rangeForHyperparamsObj.nbrOfHiddenLayersDict.get('min')
    nbrOfLayersMMax = rangeForHyperparamsObj.nbrOfHiddenLayersDict.get('max')
    nbrOfLayersArray = np.random.random_integers(nbrOfLayersMin, nbrOfLayersMMax, nbrOfModels)

    # 2. Choose number of nodes per Layer
    nbrOfNodesMin = rangeForHyperparamsObj.nbrOfHiddenUnitsDict.get('min')
    nbrOfNodesMax = rangeForHyperparamsObj.nbrOfHiddenUnitsDict.get('max')
    # This results the same number of nodes per Layer for each model
    nbrOfNodesArray = np.random.random_integers(nbrOfNodesMin, nbrOfNodesMax, nbrOfModels)

    # activationArray
    indexForActivationArray = np.random.random_integers(0, len(rangeForHyperparamsObj.activationArray) - 1,
                                                        nbrOfModels)
    # dropOutArray: The dropout rate for each model
    dropOutArray = np.random.random_sample(nbrOfModels)
    # lossFunction
    lossFunctionArray = np.random.choice(rangeForHyperparamsObj.lossFunctionArray, nbrOfModels,
                                         replace=True)
    # modelOptimizer
    modelOptimizerArray = np.random.choice(rangeForHyperparamsObj.modelOptimizerArray, nbrOfModels,
                                           replace=True)
    # Learning Rate (code from: https://www.coursera.org/learn/deep-neural-network/lecture/3rdqN/using-an-appropriate-scale-to-pick-hyperparameters Video: 02min55s)
    minLog = np.log10(rangeForHyperparamsObj.learningRateDict.get('min'))
    maxLog = np.log10(rangeForHyperparamsObj.learningRateDict.get('max'))
    exponents = (maxLog - minLog) * np.random.random_sample(
        nbrOfModels) + minLog  # code from: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.random_sample.html
    learningRateArray = np.power(10, exponents)
    # learningRateDecay
    minLrd = rangeForHyperparamsObj.learningRateDecayDict.get('min')
    maxLrd = rangeForHyperparamsObj.learningRateDecayDict.get('max')
    learningRateDecayArray = (maxLrd - minLrd) * np.random.random_sample(
        nbrOfModels) + minLrd  # code from: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.random_sample.html

    #############################################################
    # Construct a dict for each model with the above arrays
    #############################################################
    # Initialize list for HyperParamsObj (one HyperParamsObj for each model)
    hyperParamsList = list()

    # nbrOfModel times: create a HyperParamsObj (for each model one)
    for i in range(0, nbrOfModels):
        # Initialize HyperParamsObj
        tmpHyperParamsObj = HyperParamsObj()
        # Get nbrOfLayers
        tmpNbrOfLayers = nbrOfLayersArray[i]

        ###################################################
        # Store values in tmpHyperParamsObj
        ###################################################
        # nbrOfFeatures
        nbrOfFeatures = rangeForHyperparamsObj.nbrOfFeatures
        # nbrOfCategories
        nbrOfCategories = rangeForHyperparamsObj.nbrOfCategories
        # nbr of nodes in hidden layers  Create Array with length nbrOfLayersArray[i] and all values = nbrOfNodesArray[i] <<<--- This results in the same number of nodes per Layer for each model
        if tmpNbrOfLayers < 3:
            tmpHyperParamsObj.nbrOfNodesArray = [nbrOfFeatures, nbrOfCategories]
        else:
            hiddenNodesArray = np.full(tmpNbrOfLayers - 2, nbrOfNodesArray[i])
            nbrOfFeaturesAsArray = [nbrOfFeatures]
            nbrOfCategoriesAsArray = [nbrOfCategories]
            tmpHyperParamsObj.nbrOfNodesArray = np.concatenate(
                [nbrOfFeaturesAsArray, hiddenNodesArray, nbrOfCategoriesAsArray])

        # nbr of Features
        tmpHyperParamsObj.nbrOfFeatures = rangeForHyperparamsObj.nbrOfFeatures
        # learning rate
        tmpHyperParamsObj.learningRate = learningRateArray[i]
        # model optimizer
        tmpHyperParamsObj.modelOptimizer = modelOptimizerArray[i]
        # Activation function: Choose from the range of activation functions with the above randomly created indexes the activation Function for this model
        tmpHyperParamsObj.activationFunction = rangeForHyperparamsObj.activationArray[
            indexForActivationArray[i]]
        # Activation function for all layers of one model
        tmpHyperParamsObj.activationFunction = rangeForHyperparamsObj.activationArray[
            indexForActivationArray[i]]
        # Drop out rate for all layers of one model
        tmpHyperParamsObj.dropOutRate = dropOutArray[i]
        # Loss function
        tmpHyperParamsObj.lossFunction = lossFunctionArray[i]
        # learning rate decay
        tmpHyperParamsObj.learningRateDecay = learningRateDecayArray[i]
        ######################################################################
        # Add tmpHyperParamsObj to list (one tmpHyperParamsObj for each model)
        ######################################################################
        hyperParamsList.append(tmpHyperParamsObj)

    # Return the list of dicts, each with hyperparams for each model
    if len(hyperParamsList) == 1:
        return hyperParamsList[0]
    else:
        return hyperParamsList