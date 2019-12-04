from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.dbInteraction.ModelInteractionModel import ModelInteractionModel
from astropy.table import Table, Column
import numpy as np
import time
import matplotlib.pyplot as plt

from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader


class OptimizeParamsModel:

    def __init__(self, xTrain, yTrain, xTest, yTest, rangeForHyperParamsObj, nbrOfModels):
        self.modelList = list()
        self.successRate = list()
        self.resultData = None
        self.runningTimeList = list()
        self.xTrain = xTrain
        self.yTrain = yTrain
        self.xTest = xTest
        self.yTest = yTest
        self.rangeForHyperparamsObj = rangeForHyperParamsObj
        self.nbrOfModels = nbrOfModels
        self.hyperParamsObjList = self.createHyperParamsListRandom()


    def estimateTime(self):
        return EstimateTimeModel.estimateTime(hyperParams=self.hyperParamsObjList)

    def createHyperParamsListRandom(self):
        """This method takes as input the number of models to be created and ranges for hyperparameters and returns a
        list of dicts where each dict contains the hyperparams for one model. The input object has to be a dict with the
        following names as key and as values an integer array with min, max values to specify a range OR a string array
        to specify optimizers or lossFunctions.
        Keys for this dict: numberOfLayers, numberOfNodesPerLayer, activationFunctionPerLayer,
        dropOutRatePerLayer, lossFunction, modelOptimizer, learningRate, learningRateDecay. Random: The parameter
        values will be chosen randomly from the above ranges.
        """

        #############################################################
        # Prepare arrays with values for dicts
        #############################################################

        # 1. Choose number of layers
        nbrOfLayersMin = self.rangeForHyperparamsObj.nbrOfHiddenLayersDict.get('min')
        nbrOfLayersMMax = self.rangeForHyperparamsObj.nbrOfHiddenLayersDict.get('max')
        nbrOfLayersArray = np.random.random_integers(nbrOfLayersMin, nbrOfLayersMMax, self.nbrOfModels)

        # 2. Choose number of nodes per Layer
        nbrOfNodesMin = self.rangeForHyperparamsObj.nbrOfHiddenUnitsDict.get('min')
        nbrOfNodesMax = self.rangeForHyperparamsObj.nbrOfHiddenUnitsDict.get('max')
        # This results the same number of nodes per Layer for each model
        nbrOfNodesArray = np.random.random_integers(nbrOfNodesMin, nbrOfNodesMax, self.nbrOfModels)

        # activationArray
        indexForActivationArray = np.random.random_integers(0, len(self.rangeForHyperparamsObj.activationArray) - 1, self.nbrOfModels)
        # dropOutArray: The dropout rate for each model
        dropOutArray = np.random.random_sample(self.nbrOfModels)
        # lossFunction
        lossFunctionArray = np.random.choice(self.rangeForHyperparamsObj.lossFunctionArray, self.nbrOfModels, replace=True)
        # modelOptimizer
        modelOptimizerArray = np.random.choice(self.rangeForHyperparamsObj.modelOptimizerArray, self.nbrOfModels, replace=True)
        # Learning Rate (code from: https://www.coursera.org/learn/deep-neural-network/lecture/3rdqN/using-an-appropriate-scale-to-pick-hyperparameters Video: 02min55s)
        minLog = np.log10(self.rangeForHyperparamsObj.learningRateDict.get('min'))
        maxLog = np.log10(self.rangeForHyperparamsObj.learningRateDict.get('max'))
        exponents = (maxLog - minLog) * np.random.random_sample(self.nbrOfModels) + minLog    # code from: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.random_sample.html
        learningRateArray = np.power(10, exponents)
        # learningRateDecay
        minLrd = self.rangeForHyperparamsObj.learningRateDecayDict.get('min')
        maxLrd = self.rangeForHyperparamsObj.learningRateDecayDict.get('max')
        learningRateDecayArray = (maxLrd - minLrd) * np.random.random_sample(self.nbrOfModels) + minLrd   # code from: https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.random_sample.html

        #############################################################
        # Construct a dict for each model with the above arrays
        #############################################################
        # Initialize list for HyperParamsObj (one HyperParamsObj for each model)
        hyperParamsList = list()

        # nbrOfModel times: create a HyperParamsObj (for each model one)
        for i in range(0,self.nbrOfModels):
            # Initialize HyperParamsObj
            tmpHyperParamsObj = HyperParamsObj()
            # Get nbrOfLayers
            tmpNbrOfLayers = nbrOfLayersArray[i]

            ###################################################
            # Store values in tmpHyperParamsObj
            ###################################################
            # nbrOfFeatures
            nbrOfFeatures = self.rangeForHyperparamsObj.nbrOfFeatures
            # nbrOfCategories
            nbrOfCategories = self.rangeForHyperparamsObj.nbrOfCategories
            # nbr of nodes in hidden layers  Create Array with length nbrOfLayersArray[i] and all values = nbrOfNodesArray[i] <<<--- This results in the same number of nodes per Layer for each model
            if tmpNbrOfLayers < 3:
                tmpHyperParamsObj.nbrOfNodesArray = [nbrOfFeatures, nbrOfCategories]
            else:
                hiddenNodesArray = np.full(tmpNbrOfLayers - 2, nbrOfNodesArray[i])
                nbrOfFeaturesAsArray = [nbrOfFeatures]
                nbrOfCategoriesAsArray = [nbrOfCategories]
                tmpHyperParamsObj.nbrOfNodesArray = np.concatenate([nbrOfFeaturesAsArray, hiddenNodesArray, nbrOfCategoriesAsArray])

            # nbr of Features
            tmpHyperParamsObj.nbrOfFeatures = self.rangeForHyperparamsObj.nbrOfFeatures
            # learning rate
            tmpHyperParamsObj.learningRate = learningRateArray[i]
            # model optimizer
            tmpHyperParamsObj.modelOptimizer = modelOptimizerArray[i]
            # Activation function: Choose from the range of activation functions with the above randomly created indexes the activation Function for this model
            tmpHyperParamsObj.activationFunction = self.rangeForHyperparamsObj.activationArray[indexForActivationArray[i]]
            # Activation function for all layers of one model
            tmpHyperParamsObj.activationFunction = self.rangeForHyperparamsObj.activationArray[indexForActivationArray[i]]
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
        return hyperParamsList

    def evaluateModels(self):
        """This method takes as input a list of HyperParamsObj (a HyperParamsObj for every model to create). It creates,
        trains and evaluates models basing on this list of HyperParamsObj and stores the time measurements for later
        time predictions. """

        # Loop through list with hyperParamsObj for each model
        l = len(self.hyperParamsObjList)
        for i in range(0, l):
            hyperParamsObj = self.hyperParamsObjList[i]
            startTime = time.clock()
            print("################################ Building of model", i+1, "of", l, "started. ################################")
            #####################################################################################
            # create model
            #####################################################################################
            model = MachineLearningModel(hyperParamsObj, "unnamed Model")
            model.createNetwork()
            print("OptimizeParamsModel.evaluateModels: Model created.", model)

            #####################################################################################
            # Train and evaluate model
            #####################################################################################
            # train model
            # last parameter = batch size
            print("OptimizeParamsModel.evaluateModels: Shape xTrain: ", np.shape(self.xTrain))
            print("OptimizeParamsModel.evaluateModels: Shape yTrain: ", np.shape(self.yTrain))
            model.trainNetwork(self.xTrain, self.yTrain)

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
            self.modelList.append(model)

            # store success Rate (Percentage of correct predictions)
            self.successRate.append(1-errorSum/len(comparisonArray))

            # Store running time measurement
            runningTime = time.clock() - startTime
            self.runningTimeList.append(runningTime)
            # print progress of loop
            print("************ Model", i+1, "from", l, "built. *************")

        #####################################################################################
        # Save running time measurements
        #####################################################################################
        sl = SaverLoader()
        sl.saveTimeMeasurementData(self.hyperParamsObjList, self.runningTimeList)

        #####################################################################################
        # Save running time accuracy
        #####################################################################################
        # get running time accuracy
        etm = EstimateTimeModel()
        estimate = etm.estimateTime(self.hyperParamsObjList)
        actualRunningTime = sum(self.runningTimeList)
        # Accuracy: Difference between estimate in relation to actual time and 1

        accuracy = abs(1-estimate/actualRunningTime)
        # store accuracy
        sl = SaverLoader()
        sl.storeEstimateTimeAccuracy(accuracy)

        #####################################################################################
        # Save model to filesystem
        #####################################################################################
        # pd = DatabaseConnector()
        # projectID = 666                                # delete after implementation of projectID   <-----------------------------------------------------------------
        # pd.saveModel(projectID, model)                 # <----------------- Create model table in database first --------------------------------------------------------

        #####################################################################################
        # Print stuff for debugging
        #####################################################################################
        print("######################### Stats from OptimizeModel.evaluateModels ############################")
        print("HyperParams: nbrOfLayers")
        for h in self.hyperParamsObjList:
            print(len(h.nbrOfNodesArray))

        for h in self.hyperParamsObjList:
            print(h.nbrOfNodesArray)

        for h in self.hyperParamsObjList:
            print(h.learningRate)

        print("Estimated time: ", estimate, " actual time: ", actualRunningTime)

    def getResultData(self):
        """Creates a table with all results. Columns: nbrOfLayers, nbrOfNodesPerHiddenLayer, activationFunction,
        dropOutRate, lossFunction, modelOptimizer, learningRate, learningRateDecay, successRate, Rows: values for each
        model. The table will be stored in self.resultData."""

        # fill result table with data
        l = len(self.modelList)
        rows = []                       # code for table construction from https://docs.astropy.org/en/stable/table/#construct-table
        # Create array with cols = hyperParams & error; rows = values per model
        for i in range(0, l):
            # get model
            model = self.modelList[i]
            h = model.hyperParamsObj

            # get data for each model
            nbrOfLayers = len(h.nbrOfNodesArray)
            if nbrOfLayers < 3:
                nbrOfNodesPerHiddenLayer = 0
            else: nbrOfNodesPerHiddenLayer = h.nbrOfNodesArray[1]
            activationFunction = h.activationFunction
            dropOutRate = h.dropOutRate
            lossFunction = h.lossFunction
            modelOptimizer = h.modelOptimizer
            learningRate = h.learningRate
            learningRateDecay = h.learningRateDecay
            successRate = self.successRate[i]

            # create new row
            row = (nbrOfLayers, nbrOfNodesPerHiddenLayer, activationFunction, dropOutRate, lossFunction, modelOptimizer,
                   learningRate, learningRateDecay, successRate)

            # add row to row object
            rows.append(row)

        # Create table
        t = Table(rows=rows, names=['nbrOfLayers', 'nbrOfNodesPerHiddenLayer', 'activationFunction', 'dropOutRate',
                                    'lossFunction', 'modelOptimizer', 'learningRate', 'learningRateDecay', 'successRate'])
        # Store table in self
        self.resultData = t

    def getBestModel(self):
        """Checks if self.modelList is empty (that means if Optimization was executed). If not empty, it returns the
        model with the max success rate."""
        # Get best model is only possible if self.model list is not empty
        if not self.modelList:
            maxSuccessIndex = np.argmax(self.successRate)
            return self.modelList[maxSuccessIndex]
        else:
            raise Exception("OptimizeParamsModel.modelList is empty")

    def visualizeHyperparamsPerformance(self):
        t = self.resultData
        t.sort('nbrOfLayers')

        # nbrOfLayers
        plt.subplot(241)
        plt.scatter(t['nbrOfLayers'], t['successRate'])
        plt.xlabel('Number of Layers')
        plt.ylabel('Success Rate')

        # nbrOfNodesPerHiddenLayer
        plt.subplot(242)
        plt.scatter(t['nbrOfNodesPerHiddenLayer'], t['successRate'])
        plt.xlabel('Number of nodes per hidden Layer')
        plt.ylabel('Success Rate')

        # activationFunction
        plt.subplot(243)
        plt.scatter(t['activationFunction'], t['successRate'])
        plt.xlabel('Activation Function')
        plt.ylabel('Success Rate')

        # dropOutRate
        plt.subplot(244)
        plt.scatter(t['dropOutRate'], t['successRate'])
        plt.xlabel('Drop out rate')
        plt.ylabel('Success Rate')

        # lossFunction
        plt.subplot(245)
        plt.scatter(t['lossFunction'], t['successRate'])
        plt.xlabel('Loss function')
        plt.ylabel('Success Rate')

        # modelOptimizer
        plt.subplot(246)
        plt.scatter(t['modelOptimizer'], t['successRate'])
        plt.xlabel('Model optimizer')
        plt.ylabel('Success Rate')

        # learningRate
        plt.subplot(247)
        plt.scatter(t['learningRate'], t['successRate'])
        plt.xlabel('Learning rate')
        plt.ylabel('Success Rate')

        # learningRateDecay
        plt.subplot(248)
        plt.scatter(t['learningRateDecay'], t['successRate'])
        plt.xlabel('Learning rate decay')
        plt.ylabel('Success Rate')
        plt.show()

    def visualizeBestModel(self):
        t = self.resultData

        plt.subplot(241)
        plt.scatter(t['nbrOfLayers'], t['successRate'])
        plt.xlabel('Number of Layers')
        plt.ylabel('Success Rate')

