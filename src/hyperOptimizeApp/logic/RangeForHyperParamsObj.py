import numpy as np

class RangeForHyperParamsObj():

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
