from unittest import TestCase
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.persistence.ProjectDatabase import ProjectDatabase
import tensorflow as tf
import numpy as np
from tensorflow.python.keras.utils import np_utils
import datetime

class TestProjectDatabase(TestCase):



    def test_saveModel_AND_getModelByID(self):
        ########################################################
        # Create model
        ########################################################

        hp = HyperParamsObj()
        hp.nbrOfNodesArray = [784, 100, 100, 10]
        hp.activationFunction = 'sigmoid'
        hp.dropOutRate = 0.5  #
        hp.lossFunction = 'binary_crossentropy'
        hp.modelOptimizer = 'Adam'
        hp.learningRate = 0.001
        hp.learningRateDecay = 1e-6

        model = MachineLearningModel(hyperParamsObj=hp)
        model.createNetwork()

        ########################################################
        # Get training data
        ########################################################
        nbrOfCategories = 10
        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # Reshape data (cases, features)
        shapeXtrain = np.shape(x_train)
        x_train = np.reshape(x_train, (shapeXtrain[0], shapeXtrain[1] * shapeXtrain[2]))

        # Preprocess class labels (Code from: https://elitedatascience.com/keras-tutorial-deep-learning-in-python)
        y_train = np_utils.to_categorical(y_train, nbrOfCategories)

        # Rescale data 0 < data < 1
        x_train = x_train / 255.0

        ########################################################
        # Train model and make prediction
        ########################################################
        model.trainNetwork(x_train, y_train)

        checksum = sum(model.predict(x_train))

        ########################################################
        # Store model
        ########################################################
        pd = ProjectDatabase()
        date = datetime.date.today().strftime('%Y-%m-%d')
        pd.saveModel(id=666, model=model, projectID=12345)

        ########################################################
        # Get model from db
        ########################################################
        loadedModel = pd.getModelByID(666)
        checksumLoadedModel = sum(loadedModel.predict(x_train))

        self.assertEqual(checksum, checksumLoadedModel)