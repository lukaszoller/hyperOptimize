import unittest
import jsonpickle
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj


class HyperParamsObjTest(unittest.TestCase):
    def testToJsonHyperParamBlank(self):
        hyperParams = HyperParamsObj()
        hyperParamsJson = jsonpickle.encode(hyperParams)
        hyperParamsClone = jsonpickle.decode(hyperParamsJson)
        self.assertEqual(hyperParams.activationFunction, hyperParamsClone.activationFunction)
        self.assertEqual(hyperParams.dropOutRate, hyperParamsClone.dropOutRate)
        self.assertEqual(hyperParams.learningRate, hyperParamsClone.learningRate)
        self.assertEqual(hyperParams.lossFunction, hyperParamsClone.lossFunction)
        self.assertEqual(hyperParams.learningRateDecay, hyperParamsClone.learningRateDecay)
        self.assertEqual(hyperParams.modelOptimizer, hyperParamsClone.modelOptimizer)
        self.assertEqual(hyperParams.nbrOfNodesArray, hyperParamsClone.nbrOfNodesArray)

    def testToJsonHyperParamFilled(self):
        hyperParams = HyperParamsObj([1, 2, 4, 6], 2, 0.9, 'loss function', 'model optimizer', 0.5, 0.6)
        hyperParamsJson = jsonpickle.encode(hyperParams)
        hyperParamsClone = jsonpickle.decode(hyperParamsJson)
        self.assertEqual(hyperParams.activationFunction, hyperParamsClone.activationFunction)
        self.assertEqual(hyperParams.dropOutRate, hyperParamsClone.dropOutRate)
        self.assertEqual(hyperParams.learningRate, hyperParamsClone.learningRate)
        self.assertEqual(hyperParams.lossFunction, hyperParamsClone.lossFunction)
        self.assertEqual(hyperParams.learningRateDecay, hyperParamsClone.learningRateDecay)
        self.assertEqual(hyperParams.modelOptimizer, hyperParamsClone.modelOptimizer)
        self.assertEqual(hyperParams.nbrOfNodesArray, hyperParamsClone.nbrOfNodesArray)


if __name__ == '__main__':
    unittest.main()
