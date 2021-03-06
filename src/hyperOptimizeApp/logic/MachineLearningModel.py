import numpy as np
import tensorflow as tf


class MachineLearningModel:
    # Constructor for new model
    def __init__(self, hyperParamsObj, modelName='', modelId=0, model=tf.keras.models.Sequential()):
        self.modelName = modelName
        self.model = model
        print("len(MachineLearningModel.model.layers): ", len(self.model.layers))
        self.hyperParamsObj = hyperParamsObj
        self.modelId = modelId
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
        modelOptimizerObj = getattr(tf.keras.optimizers, modelOptimizer)(lr=learningRate, decay=decay)

        self.model.compile(optimizer=modelOptimizerObj, loss=lossFunction, metrics=['accuracy'])
        print("MachineLearningModel.createNetwork: model compiled")
        print("len(MachineLearningModel.model.layers): ", len(self.model.layers))
        self.model.summary()

    def getNbrOfFeatures(self):
        if self.hyperParamsObj.nbrOfNodesArray[0] > 0:
            return self.hyperParamsObj.nbrOfNodesArray[0]
        else:
            print("MachineLearningModel.self.hyperParamsObj.nbrOfNodesArray[0] == 0 or is empty.")

    # def trainNetwork(self, x, y, epochs):
    #     self.model.fit(x, y, epochs)

    def trainNetwork(self, x, y):
        self.model.fit(x, y, verbose=1, epochs=3, use_multiprocessing=False) #Multiprocessing = true has no effect on running time

    def evaluateModel(self, x, y):
        return self.model.evaluate(x, y)


    def optimizeHyperparameters(self):
        print("Empty method: MachineLearningModel.optimizeHyperparameters")

    def setParamsManually(self, params):
        self.hyperParameter = params

    def getPredictionData(self, predictionData):
        self.predictionData = predictionData

    def predict(self, x):
        return np.round(np.array(self.model.predict(x)), decimals=0)

    def to_json(self):
        return self.model.to_json()

    def resetModel(self):
        self.model = tf.keras.models.Sequential()
