import tensorflow as tf
import numpy as np


class MachineLearningModel:
    # Constructor for new model
    def __init__(self):
        self.model = tf.keras.models.Sequential()
        print("MachineLearningModel: MachineLearningModel-constructor executed: ", self.model)

    ## for available activation functions check https://keras.io/activations/
    ## for available loss functions check https://keras.io/losses/
    def createNetwork(self, hyperParamsObj):
        nbrOfNodesArray = hyperParamsObj.nbrOfNodesArray
        activationArray = hyperParamsObj.activationArray
        dropOutArray = hyperParamsObj.dropOutArray
        lossFunction = hyperParamsObj.lossFunction
        modelOptimizer = hyperParamsObj.modelOptimizer
        learningRate = hyperParamsObj.learningRate
        decay = hyperParamsObj.learningRateDecay



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
                self.model.add(tf.keras.layers.Dropout(dropOutArray[i]))
                print("Layer", i + 1, "of", len(nbrOfNodesArray), "built.")

        # Add last layer
        self.model.add(tf.keras.layers.Dense(input_dim=nbrCategories, units=nbrOfUnitsArray[-1]))

        # Specify activation function
        self.model.add(tf.keras.layers.Activation('sigmoid'))

        # define modelOptimizer and learning rate
        modelOptimizerObj = getattr(tf.keras.optimizers, modelOptimizer)(lr=learningRate, decay= decay)

        self.model.compile(optimizer=modelOptimizerObj, loss=lossFunction)
        print("MachineLearningModel.createNetwork: model compiled")
        self.model.summary()

    def trainNetwork(self, x, y, epochs):
        self.model.fit(x, y, epochs)

    def trainNetwork(self, x, y):
        print("MachineLearningModel.trainNetwork: Shape of x:", np.shape(x))
        print("MachineLearningModel.trainNetwork: Shape of y:", np.shape(y))
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

a = [1,2,3,3,4]
b = np.append(a, 10)
print(b[-1])