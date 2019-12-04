import json


class HyperParamsObj:

    def __init__(self, nbrOfNodesArray=None, activationFunction=0, dropOutRate=0, lossFunction='', modelOptimizer='',
                 learningRate=0, learningRateDecay=0):
        self.nbrOfNodesArray = nbrOfNodesArray
        self.activationFunction = activationFunction  #mal noch lassen
        self.dropOutRate = dropOutRate   #
        self.lossFunction = lossFunction
        self.modelOptimizer = modelOptimizer
        self.learningRate = learningRate
        self.learningRateDecay = learningRateDecay
