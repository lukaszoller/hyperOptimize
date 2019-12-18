from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from astropy.table import Table, Column
import numpy as np
import time
import matplotlib.pyplot as plt
from src.hyperOptimizeApp.persistence.FileSystemRepository import FileSystemRepository
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import createHyperParamsListRandom
import tensorflow as tf


class OptimizeParamsModel:

    def __init__(self, xTrain, yTrain, xTest, yTest, rangeForHyperParamsObj, nbrOfModels):
        self.bestModel = None
        self.successRateList = list()
        self.resultData = None
        self.runningTimeList = list()
        self.xTrain = xTrain
        self.yTrain = yTrain
        self.xTest = xTest
        self.yTest = yTest
        self.rangeForHyperparamsObj = rangeForHyperParamsObj
        self.nbrOfModels = nbrOfModels
        self.hyperParamsObjList = createHyperParamsListRandom(self.rangeForHyperparamsObj, self.nbrOfModels)

    def evaluateModels(self):
        """This method takes as input a list of HyperParamsObj (a HyperParamsObj for every model to create). It creates,
        trains and evaluates models basing on this list of HyperParamsObj and stores the time measurements for later
        time predictions. """

        # Loop through list with hyperParamsObj for each model
        l = len(self.hyperParamsObjList)
        scoreList = []
        scoreBaseList = []
        for i in range(0, l):
            hyperParamsObj = self.hyperParamsObjList[i]
            print("################################ HyperParameters of model", i+1, "of", l, ":. ###############################")
            print("Number of Hidden Layers: " + str(len(hyperParamsObj.nbrOfNodesArray)))
            print("Number of Nodes per Layer: " + str(hyperParamsObj.nbrOfNodesArray[1]))
            print("Activation Function: " + str(hyperParamsObj.activationFunction))
            print("Dropout Rate: " + str(hyperParamsObj.dropOutRate))
            print("Learning Rate: " + str(hyperParamsObj.learningRate))
            print("Learning Rate Decay: " + str(hyperParamsObj.learningRateDecay))
            print("Loss Function: " + str(hyperParamsObj.lossFunction))
            print("Model Optimizer: " + str(hyperParamsObj.modelOptimizer))
            startTime = time.clock()
            print("################################ Building of model", i+1, "of", l, "started. ################################")
            #####################################################################################
            # create model
            #####################################################################################
            model = MachineLearningModel(hyperParamsObj, "unnamed Model", modelId=0, model=tf.keras.models.Sequential())
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
            # Evaluate with test data todo: maybe delete this after tests
            #####################################################################################
            # evaluate data
            scores = model.evaluateModel(self.xTest, self.yTest)
            print(scores)
            print("%s: %.2f%%" % (model.model.metrics_names[1], scores[1] * 100))
            scoreList.append(str("%s: %.2f%%" % (model.model.metrics_names[1], scores[1] * 100)))
            scoreBaseList.append(scores[1])

            tmpSuccess = scores[1]
            # self.successRateList.append(tmpSuccess)
            #####################################################################################
            # Predict with test data
            #####################################################################################
            # predict data
            y_predict = model.predict(self.xTest)

            if hyperParamsObj.nbrOfNodesArray[-1] == 1:
                y_PredictOneCol = np.round(y_predict, decimals=0)
                y_TestOneCol = self.yTest
            else:
                y_PredictOneCol = np.argmax(y_predict, axis=1)
                y_TestOneCol = np.argmax(self.yTest, axis=1)

            print(y_PredictOneCol)
            print(y_TestOneCol)
            trainEqualTestArray = y_PredictOneCol == y_TestOneCol
            print(trainEqualTestArray)
            successSum = np.sum(trainEqualTestArray)

            # store success Rate (Percentage of correct predictions)
            tmpSuccess = successSum/len(trainEqualTestArray)
            self.successRateList.append(tmpSuccess)

            #####################################################################################
            # Save model if better than last, else drop
            #####################################################################################
            # get successRate of last model
            # if this is first loop, last successRate = 0
            if len(self.successRateList) == 1:
                lastSuccess = 0
            else:  # get success of second last item
                lastSuccess = self.successRateList.__getitem__(len(self.successRateList) - 2)
            # Save model if tmpSuccess (of this loop) is higher than success of last model
            if tmpSuccess > lastSuccess:
                self.bestModel = model

            # Store running time measurement
            runningTime = time.clock() - startTime
            self.runningTimeList.append(runningTime)
            # print progress of loop
            print("************ Model", i+1, "from", l, "built. *************")
            print("len(model.layers: ", len(model.model.layers))
            print("model.layers: ", model.model.layers)

        #####################################################################################
        # Save running time measurements
        #####################################################################################
        fl = FileSystemRepository()
        fl.saveTimeMeasurementData(self.hyperParamsObjList, self.runningTimeList)

        #####################################################################################
        # Save running time accuracy
        #####################################################################################
        # get running time accuracy
        etm = EstimateTimeModel()
        stringEstimate, numberEstimate = etm.estimateTime(self.hyperParamsObjList)
        actualRunningTime = sum(self.runningTimeList)
        # Accuracy: Difference between estimate in relation to actual time and 1

        accuracy = abs(1-numberEstimate/actualRunningTime)
        # store accuracy
        fl.storeEstimateTimeAccuracy(accuracy)

        #####################################################################################
        # Print stuff for debugging
        #####################################################################################
        print("######################### Stats from OptimizeModel.evaluateModels ############################")
        print("HyperParams: nbrOfLayers")
        for h in self.hyperParamsObjList:
            print("Length Array: " + str(len(h.nbrOfNodesArray)))
            print("Array form: " + str(h.nbrOfNodesArray))
            print("Learning rate: " + str(h.learningRate))

        print("Estimated time: ", stringEstimate, " actual time: ", actualRunningTime)
        print("######################### Stats from ScoreList ############################")
        print(scoreList)

        self.createResultData()

    def createResultData(self):
        # fill result table with data
        l = len(self.hyperParamsObjList)
        rows = []  # code for table construction from https://docs.astropy.org/en/stable/table/#construct-table
        # Create array with cols = hyperParams & error; rows = values per model
        for h in self.hyperParamsObjList:
            # get data for each model
            nbrOfLayers = len(h.nbrOfNodesArray)
            if nbrOfLayers < 3:
                nbrOfNodesPerHiddenLayer = 0
            else:
                nbrOfNodesPerHiddenLayer = h.nbrOfNodesArray[1]
            activationFunction = h.activationFunction
            dropOutRate = h.dropOutRate
            lossFunction = h.lossFunction
            modelOptimizer = h.modelOptimizer
            learningRate = h.learningRate
            learningRateDecay = h.learningRateDecay

            # create new row
            row = (nbrOfLayers, nbrOfNodesPerHiddenLayer, activationFunction, dropOutRate, lossFunction, modelOptimizer,
                   learningRate, learningRateDecay)

            # add row to row object
            rows.append(row)

        # Create table
        t = Table(rows=rows, names=['nbrOfLayers', 'nbrOfNodesPerHiddenLayer', 'activationFunction', 'dropOutRate',
                                    'lossFunction', 'modelOptimizer', 'learningRate', 'learningRateDecay'])

        # add column with successRate
        col = Column(data=self.successRateList, name='successRate')
        t.add_column(col)

        # Store table in self
        self.resultData = t


    # def getResultData(self):
    #     """Creates a table with all results. Columns: nbrOfLayers, nbrOfNodesPerHiddenLayer, activationFunction,
    #     dropOutRate, lossFunction, modelOptimizer, learningRate, learningRateDecay, successRate, Rows: values for each
    #     model. The table will be stored in self.resultData."""
    #
    #     # fill result table with data
    #     l = len(self.successRateList)
    #     rows = []                       # code for table construction from https://docs.astropy.org/en/stable/table/#construct-table
    #     # Create array with cols = hyperParams & error; rows = values per model
    #     for i in range(0, l):
    #         # get model
    #         model = self.modelList[i]
    #         h = model.hyperParamsObj
    #
    #         # get data for each model
    #         nbrOfLayers = len(h.nbrOfNodesArray)
    #         if nbrOfLayers < 3:
    #             nbrOfNodesPerHiddenLayer = 0
    #         else: nbrOfNodesPerHiddenLayer = h.nbrOfNodesArray[1]
    #         activationFunction = h.activationFunction
    #         dropOutRate = h.dropOutRate
    #         lossFunction = h.lossFunction
    #         modelOptimizer = h.modelOptimizer
    #         learningRate = h.learningRate
    #         learningRateDecay = h.learningRateDecay
    #         successRate = self.successRateList[i]
    #
    #         # create new row
    #         row = (nbrOfLayers, nbrOfNodesPerHiddenLayer, activationFunction, dropOutRate, lossFunction, modelOptimizer,
    #                learningRate, learningRateDecay, successRate)
    #
    #         # add row to row object
    #         rows.append(row)
    #
    #     # Create table
    #     t = Table(rows=rows, names=['nbrOfLayers', 'nbrOfNodesPerHiddenLayer', 'activationFunction', 'dropOutRate',
    #                                 'lossFunction', 'modelOptimizer', 'learningRate', 'learningRateDecay', 'successRate'])
    #     # Store table in self
    #     self.resultData = t

    def getBestModel(self):
        """Checks if self.modelList is empty (that means if Optimization was executed). If not empty, it returns the
        model with the max success rate."""
        # Get best model is only possible if self.model list is not empty
        # if not self.modelList:  # if list is empty
        #     raise Exception("OptimizeParamsModel.modelList is empty")
        # else:
        #     maxSuccessIndex = np.argmax(self.successRateList)
        #     return self.modelList[maxSuccessIndex]
        if self.bestModel is None:
            raise Exception("No best model found")
        return self.bestModel

    def visualizeHyperparamsPerformance(self):
        """Creates a figure which can be displayed in a gui-window. Shows plot also in dev environment if not disabled."""
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

    def getResultsPlot(self):
        """Creates a figure which can be displayed in a gui-window. Shows plot also in dev environment if not disabled."""
        t = self.resultData
        t.sort('nbrOfLayers')

        figure = plt.figure(figsize=(15,7))
        ax1 = figure.add_subplot(241)
        ax1.scatter(t['nbrOfLayers'], t['successRate'])
        plt.xlabel('Number of layers')
        plt.ylabel('Success Rate')

        ax2 = figure.add_subplot(242)
        ax2.scatter(t['nbrOfNodesPerHiddenLayer'], t['successRate'])
        plt.xlabel('Number of hidden nodes per layer')
        plt.ylabel('Success Rate')

        ax3 = figure.add_subplot(243)
        ax3.scatter(t['activationFunction'], t['successRate'])
        plt.xlabel('Activation function')
        plt.ylabel('Success Rate')

        ax4 = figure.add_subplot(244)
        ax4.scatter(t['dropOutRate'], t['successRate'])
        plt.xlabel('Drop out rate')
        plt.ylabel('Success Rate')

        ax5 = figure.add_subplot(245)
        ax5.scatter(t['lossFunction'], t['successRate'])
        plt.xlabel('Loss function')
        plt.ylabel('Success Rate')

        ax6 = figure.add_subplot(246)
        ax6.scatter(t['modelOptimizer'], t['successRate'])
        plt.xlabel('Model optimizer')
        plt.ylabel('Success Rate')

        ax7 = figure.add_subplot(247)
        ax7.scatter(t['learningRate'], t['successRate'])
        plt.xlabel('Learning rate')
        plt.ylabel('Success Rate')

        ax8 = figure.add_subplot(248)
        ax8.scatter(t['learningRateDecay'], t['successRate'])
        plt.xlabel('Learning rate decay')
        plt.ylabel('Success Rate')

        figure.tight_layout()

        # return figure
        return figure

    def visualizeBestModel(self):
        t = self.resultData

        plt.subplot(241)
        plt.scatter(t['nbrOfLayers'], t['successRate'])
        plt.xlabel('Number of Layers')
        plt.ylabel('Success Rate')

