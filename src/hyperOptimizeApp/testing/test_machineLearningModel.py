from unittest import TestCase
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj

################################################################
# Test createNetwork()
################################################################

class TestMachineLearningModel():

    def test_createNetwork(self):
        # DropOutRate = 1 --> all Nodes will be dropped
        nbrOfNodesArray = [2 ,100, 100, 2]
        activationArray = ['sigmoid', 'sigmoid', 'sigmoid', 'sigmoid']
        dropOutArray = [0.5, 0.5, 0.4, 0.4]
        lossFunction = 'binary_crossentropy'
        modelOptimizer = 'Adam'
        learningRate = 0.001
        decay = 1e-6
        machineLearningModel = MachineLearningModel()

        hyperParamsObj = HyperParamsObj()
        hyperParamsObj.nbrOfNodesArray = nbrOfNodesArray
        hyperParamsObj.activationArray = activationArray
        hyperParamsObj.dropOutArray = dropOutArray
        hyperParamsObj.lossFunction = lossFunction
        hyperParamsObj.modelOptimizer = modelOptimizer
        hyperParamsObj.learningRate = learningRate
        hyperParamsObj.learningRateDecay = decay

        machineLearningModel.createNetwork(hyperParamsObj)

t = TestMachineLearningModel()
t.test_createNetwork()


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
