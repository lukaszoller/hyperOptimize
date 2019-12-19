from unittest import TestCase
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
import tensorflow as tf

################################################################
# Test createNetwork()
################################################################

class TestMachineLearningModel():

    def test_createNetwork(self):
        """If this function runs, the MachineLearningModel will be built correctly with a HyperparamsObj."""
        # DropOutRate = 1 --> all Nodes will be dropped
        nbrOfNodesArray = [2, 100, 100, 2]
        activationFunction = 'sigmoid'
        dropOutRate = 0.01
        lossFunction = 'binary_crossentropy'
        modelOptimizer = 'Adam'
        learningRate = 0.001
        decay = 1e-6

        hyperParamsObj = HyperParamsObj()
        hyperParamsObj.nbrOfNodesArray = nbrOfNodesArray
        hyperParamsObj.activationFunction = activationFunction
        hyperParamsObj.dropOutRate = dropOutRate
        hyperParamsObj.lossFunction = lossFunction
        hyperParamsObj.modelOptimizer = modelOptimizer
        hyperParamsObj.learningRate = learningRate
        hyperParamsObj.learningRateDecay = decay

        machineLearningModel = MachineLearningModel(hyperParamsObj, modelName='', modelId=0, model=tf.keras.models.Sequential())

        machineLearningModel.createNetwork()

t = TestMachineLearningModel()
t.test_createNetwork()

