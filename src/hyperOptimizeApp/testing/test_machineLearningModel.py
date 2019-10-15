from unittest import TestCase
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel

################################################################
# Test createNetwork()
################################################################

class TestMachineLearningModel():

    def test_createNetworkDropOutOne(self):
        # DropOutRate = 1 --> all Nodes will be dropped
        nbrOfNodesArray = [2 ,100, 100, 2]
        activationArray = ['sigmoid', 'sigmoid', 'sigmoid', 'sigmoid']
        dropOutArray = [0.5, 0.5, 0.4, 0.4]
        lossFunction = 'binary_crossentropy'
        modelOptimizer = 'Adam'
        learningRate = 0.001
        decay = 1e-6
        nbrCategories = 1
        machineLearningModel = MachineLearningModel()

        machineLearningModel.createNetwork(nbrOfNodesArray, activationArray, dropOutArray, lossFunction, modelOptimizer,
                                           learningRate, decay)

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
