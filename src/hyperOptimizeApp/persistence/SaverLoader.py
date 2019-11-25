from src.hyperOptimizeApp.persistence.DatabaseConnector import DatabaseConnector
import numpy as np
import pandas as pd
import cpuinfo


class SaverLoader:

    fileName = 'estTimeData.csv'
    projectDb = DatabaseConnector()

    def __init__(self):
        self.estimateTimeAccuracyList = list()           # delete this after db implementation of running time accuracy

    def setFileName(self, fileName):
        self.fileName = fileName

    def getEstTimeData(self):
        """ Returns two arrays. A 2D array x containing the features of the estimate time dataset and a 1D array y
        containing the actual running times of each model (row)."""
        try:
            data = np.genfromtxt(self.fileName, delimiter=',', skip_header=False)
            print("SaverLoader.getEstTimeData(): data loaded successfully.")
            print(data)
            y = data[:,-1]
            x = data[:,0:len(data[1,:])-1]
            return x,y
        except IOError:
            print("Error. Could not read file:", self.fileName)

    def saveTimeMeasurementDataOld(self, x, y):
        """Appends a new time measurement to the training dataset for the time estimation. x has to be a 1D array with
        values: nbrOfLayers, nbrOfNodesPerLayer, learningRate. y has to be a single float which contains the running time
        measurement for one model in seconds."""
        np.savetxt('estTimeData.csv', [x,y], delimiter=',')

    def saveTimeMeasurementData(self, hyperParamsObjList, timeMeasurement):
        """Appends a new time measurement to the training dataset for the time estimation. x has to be a 1D array with
        values: nbrOfLayers, nbrOfNodesPerLayer, learningRate. y has to be a single float which contains the running time
        measurement for one model in seconds."""

        estTimeDataFileName = 'estTimeData.csv'
        # Prepare data (convert hyperParamsList to Array with 3 cols (nbrOfLayers, nbrOfNodesPerLayer, leraning Rate)
        hyperParamsData = self.hyperParamsListToData(hyperParamsObjList)
        # Add cpu speed data to hyperParamsData     <----- Next 3 Lines of code used exacly like here in EstimateTimeModel.estimateTime
        cpuSpeed = cpuinfo.get_cpu_info()['hz_actual_raw'][0]
        newLineWithCpuSpeed = np.full((len(hyperParamsData[:, 0]), 1), cpuSpeed)
        hyperParamsData = np.append(hyperParamsData, newLineWithCpuSpeed, axis=1)

        # Get old data
        (x,y) = self.getEstTimeData()

        print(x)
        print(y)

                   # Append new data to old data
        xNew = np.append(x, hyperParamsData, axis=0)
        yNew = np.append(y, timeMeasurement)

        newDataToWrite = np.column_stack((xNew, yNew))

        # Save data to csv
        np.savetxt(estTimeDataFileName, newDataToWrite, delimiter=',')

    def hyperParamsListToData(self, hyperParamsObjList):
        """This method converts hyperParamsObjList, a list of hyperParamsObj where every obj stands for the
        hyperparams of one model, to a 2D Array where each row contains information of one model (columns:
        1.nbrOfLayers, 2. nbrOfNodesPerLayer, 3. learningRate).
        This 2D array can be used:
         1. to get an estimate for the running time to construct, train and evaluate the models from this list.
         2. to add the array to the training data for the time estimation."""
        # Counts all dicts in hyperParamsList (a list of dict, for every model 1 dict)
        # Initialize a list with 3 columns and len = len(hyperParamsObjList)
        hyperParamsDataList = np.zeros((len(hyperParamsObjList), 3))
        # loop through all hyperParamsObjects
        for i in range(0, len(hyperParamsObjList)):
            h = hyperParamsObjList[i]
            # add nbr of Layers
            hyperParamsDataList[i, 0] = len(h.nbrOfNodesArray)
            # add nbr of nodes per hidden layer (hidden layer start from index = 1, 0st layer is input layer)
            hyperParamsDataList[i, 1] = h.nbrOfNodesArray[1]
            # add nbr of nodes per Layer
            hyperParamsDataList[i, 2] = h.learningRate

        # Old code delete if storing data of each model makes sense
        # nbrOfModels = len(hyperParamsObjList)
        # # Sum up nbr of Nodes and layers
        # sumOfNodes = 0
        # sumOfLayers = 0
        # for d in hyperParamsObjList:
        #     sumOfNodes = sumOfNodes + sum(d['nodesPerLayer'])
        #     sumOfLayers = sumOfLayers + len(d['nodesPerLayer'])

        return hyperParamsDataList

    def getProjectList(self):
        projects = self.projectDb.getAllProjects()
        # p1 = ProjectModel("FakeProject 1")
        # p2 = ProjectModel("FakeProject 2")
        # p3 = ProjectModel("FakeProject 3")
        return projects

    def saveProjectList(self):
        print("Empty method: SaverLoader.saveProjectList")


    def storeEstimateTimeAccuracy(self, accuracyValue):
        self.estimateTimeAccuracyList.append(accuracyValue)

    def saveModelToDatabase(self, model, projectId):
        self.projectDb.saveModel(model, projectId)

    def loadDataForTrainingOrPrediction(self, pathToData, firstRowIsHeader, firstColIsRownbr, nbrOfCategories=0, dataIsForTraining=False):
        """Loads data from filesystem. Takes as input pathToData (String representing full path to csv file),
        nbrOfFeatures (Size of X for training and prediction of model), firstRowIsHeader and firstColIsRownbr (both
        boolean Values).
        If nbrOfCategories is not 0 and dataIsForTraining = False, it will print an informational message to the console
        but will set nbrOfCategories to the value 0.
        If dataIsForTraining = True: Returns three np-arrays x (features of dataset), y (categories of dataset) and unmanipulatedData (x and y in
        one array with header and colnbrs (if they existed in the first place)).
        If dataIsForTraining = False: Returns only two arrays: x and unmanipulatedData."""

        # Debugging stuff delete sometimes
        print("pathToData: ", pathToData)
        print("firstRowIsHeader: ", firstRowIsHeader)
        print("firstColIsRownbr: ", firstColIsRownbr)
        print("nbrOfCategories: ", nbrOfCategories)
        print("dataIsForTraining: ", dataIsForTraining)


        # check if nbrOfCategories = 0 if dataIsForTraining = false.
        if not dataIsForTraining and nbrOfCategories != 0:
            nbrOfCategories = 0
            print("If data is used for prediction, nbrOfCategories has to be 0. Value of nbrOfCategories has been set to"
                  "0 automatically.")

        # get data
        try:
            data = np.genfromtxt(pathToData, delimiter=',', skip_header=False)
        except IOError:
            print("IOError: Could not read file: ", pathToData)

        # get dataset info
        nbrOfRows, nbrOfCols = np.shape(data)
        nbrOfFeatures = nbrOfCols - nbrOfCategories
        # return error if nbrOfFeatures is bigger than nbrOfcols
        if nbrOfFeatures > nbrOfCols:
            raise ValueError("nbrOfFeatures is bigger than nbrOfCols in dataset. nbrOfFeatures should be smaller.Probably "
                             "parameter nbrOfCategories is set wrongly.")
        # return error if nbrOfFeatures is equal to nbrOfColumns but dataset is for training (y needed)
        if nbrOfFeatures == nbrOfCols and dataIsForTraining:
            raise ValueError("nbrOfFeatures has to be smaller than nbrOfCols in dataset. Probably parameter nbrOfCategories"
                             "is set wrongly.")
        # Store data before manipulation
        unmanipulatedData = data

        # Delete first row if it is header
        if firstRowIsHeader:
            data = data[1:nbrOfRows, :]
        # Delete first col if it is colnbr
        if firstColIsRownbr:
            data = data[:,1:nbrOfCols]

        x = data[:, 0:nbrOfFeatures]

        # return data
        if dataIsForTraining:
            y = data[:, nbrOfFeatures:nbrOfCols]
            return x, y, unmanipulatedData
        else:
            return x, unmanipulatedData

