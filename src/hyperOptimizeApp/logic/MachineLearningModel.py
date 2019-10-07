import tensorflow as tf
import numpy as np


class MachineLearningModel:
    # Constructor for new model
    def __init__(self):
        pass

    # Constructor for old model
    def __init__(self):
        self.model = tf.keras.models.Sequential()

    ## for available activation functions check https://keras.io/activations/
    ## for available loss functions check https://keras.io/losses/
    def createNetwork(self,nbrFeatures, unitsArray, activationArray, dropOutArray, lossFunction, modelOptimizer):
        # Add first layer (outside loop because input_dim has to be specified
        self.model.add(tf.keras.layers.Dense(input_dim=nbrFeatures, units=unitsArray[1], activation=activationArray[1]))
        # self.model.add(tf.keras.layers.Dropout(dropOutArray[1]))

        # range(1, ...) "1" is needed to skip the first layer we built above
        for i in range(1, len(unitsArray)):
            print("Layer " + str(i) + " built.")
            self.model.add(tf.keras.layers.Dense(units=unitsArray[i]))      # activation per layer not specified
            # add dropout to all layers, except the last
            # if i != len(unitsArray)-1:
            #     self.model.add(tf.keras.layers.Dropout(dropOutArray[i]))

        self.model.add(tf.keras.layers.Activation('sigmoid'))
        self.model.compile(optimizer=modelOptimizer, loss=lossFunction)
        self.model.summary()

    def trainNetwork(self, x, y, epochs):
        self.model.fit(x, y, epochs)

    def trainNetwork(self, x, y):
        self.model.fit(x, y)

    def evaluateModel(self, x, y):
        self.model.evaluate(x, y)

    def optimizeHyperparameters(self):
        print("Empty method: MachineLearningModel.optimizeHyperparameters")

    def setParamsManually(self, params):
        self.hyperParameter = params

    def getPredictionData(self, predictionData):
        self.predictionData = predictionData

    def predict(self, x):
        return np.array(self.model.predict(x))


