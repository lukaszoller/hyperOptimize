from unittest import TestCase
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel

################################################################
# Test createNetwork()
################################################################

class TestMachineLearningModel():
    # Create model with different parameters. Check if all parameters have been set correctly
    # 1. Model with no hidden layers --> Error message
    def test_createNetworkNoHiddenLayers(self):

        nbrFeatures = 1
        unitsArrayForHiddenLayers = []
        activationArray = []
        dropOutArray = []
        lossFunction = 'binary_crossentropy'
        modelOptimizer = 'Adam'
        learningRate = 0.001
        decay = 1e-6
        nbrCategories = 1
        machineLearningModel = MachineLearningModel()
        machineLearningModel.createNetwork(nbrFeatures, unitsArrayForHiddenLayers, activationArray, dropOutArray,
                                           lossFunction, modelOptimizer, learningRate, decay, nbrCategories)
        print(len(machineLearningModel.model.layers))

    def test_createNetworkDropOutOne(self):
        # DropOutRate = 1 --> all Nodes will be dropped
        nbrFeatures = 1
        unitsArrayForHiddenLayers = [10]
        activationArray = ['sigmoid']
        dropOutArray = [1]
        lossFunction = 'binary_crossentropy'
        modelOptimizer = 'Adam'
        learningRate = 0.001
        decay = 1e-6
        nbrCategories = 1
        machineLearningModel = MachineLearningModel()
        machineLearningModel.createNetwork(nbrFeatures, unitsArrayForHiddenLayers, activationArray, dropOutArray,
                                           lossFunction, modelOptimizer, learningRate, decay, nbrCategories)
        print(len(machineLearningModel.model.layers))



t = TestMachineLearningModel()
t.test_createNetworkDropOutOne()



# class TestMachineLearningModel(TestCase):

    # def test_createNetwork(self):
    #
    # def test_trainNetwork(self):
    #     self.assertTrue(True)
    #
    # def test_trainNetwork(self):
    #     self.assertTrue(True)
    #
    # # def test_evaluateModel(self):
    #     self.fail()
    #
    # def test_optimizeHyperparameters(self):
    #     self.fail()
    #
    # def test_setParamsManually(self):
    #     self.fail()
    #
    # def test_getPredictionData(self):
    #     self.fail()
    #
    # def test_predict(self):
    #     self.fail()
