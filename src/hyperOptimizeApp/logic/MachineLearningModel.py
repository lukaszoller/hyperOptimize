import tensorflow as tf
import numpy as np


class MachineLearningModel:
    # Constructor for new model
    def __init__(self, hyperParamsObj):
        self.model = tf.keras.models.Sequential()
        self.hyperParamsObj = hyperParamsObj
        print("MachineLearningModel: MachineLearningModel-constructor executed: ", self.model)

    ## for available activation functions check https://keras.io/activations/
    ## for available loss functions check https://keras.io/losses/
    def createNetwork(self):
        """Adds layers to self.model and compiles the model."""
        nbrOfNodesArray = self.hyperParamsObj.nbrOfNodesArray
        activationFunction = self.hyperParamsObj.activationFunction
        dropOutRate = self.hyperParamsObj.dropOutRate
        lossFunction = self.hyperParamsObj.lossFunction
        modelOptimizer = self.hyperParamsObj.modelOptimizer
        learningRate = self.hyperParamsObj.learningRate
        decay = self.hyperParamsObj.learningRateDecay



        nbrFeatures = nbrOfNodesArray[0]
        nbrCategories = nbrOfNodesArray[len(nbrOfNodesArray)-1]
        # Create unitsArray (Units are the connections to the next layer, i.e. nbrOfUnits for Layer X are nbr of nodes
        # of Layer X+1
        nbrOfUnitsArray = np.append(nbrOfNodesArray[1:len(nbrOfNodesArray)], nbrCategories)

        # Add first layer (outside loop because input_dim has to be specified
        self.model.add(tf.keras.layers.Dense(input_dim=nbrFeatures, units=nbrOfUnitsArray[0]))
        # self.model.add(tf.keras.layers.Dropout(dropOutArray[1]))

        # Check if Model has hidden layers. if not, skip the loop
        if len(nbrOfNodesArray) >= 3:
            for i in range(0, len(nbrOfNodesArray)):
                self.model.add(tf.keras.layers.Dense(units=nbrOfUnitsArray[i])) #, activation=activationArray[i]))      # activation per layer not specified, performance is much worse if it is specified
                # add dropout to all layers, except the last
                self.model.add(tf.keras.layers.Dropout(dropOutRate))
                print("Layer", i + 1, "of", len(nbrOfNodesArray), "built.")

        # Add last layer
        self.model.add(tf.keras.layers.Dense(input_dim=nbrCategories, units=nbrOfUnitsArray[-1]))

        # Specify activation function
        print(activationFunction)
        self.model.add(tf.keras.layers.Activation(activationFunction))

        # define modelOptimizer and learning rate
        modelOptimizerObj = getattr(tf.keras.optimizers, modelOptimizer)(lr=learningRate, decay= decay)

        self.model.compile(optimizer=modelOptimizerObj, loss=lossFunction)
        print("MachineLearningModel.createNetwork: model compiled")
        self.model.summary()

    def trainNetwork(self, x, y, epochs):
        self.model.fit(x, y, epochs)

    def trainNetwork(self, x, y):
        self.model.fit(x, y,use_multiprocessing=False) #Multiprocessing = true has no effect on running time

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

a = [1,2,3,3,4]
b = np.append(a, 10)
print(b[-1])