from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel
import numpy as np
import csv

class SaverLoader:
    def __init__(self):
        pass

    def getEstTimeData(self):
        """ Returns two arrays. A 2D array x and a 1D array y."""
        fileName = 'estTimeData.csv'
        try:
            data = np.genfromtxt(fileName, delimiter=',', skip_header=True)
            print("SaverLoader.getEstTimeData(): data loaded successfully.")
            y = data[:,-1]
            x = data[:,0:len(data[1,:])-1]
            return x, y
        except IOError:
            print("Error. Could not read file:", fileName)

    def saveTimeMeasurementDataOld(self, x, y):
        """Appends a new time measurement to the training dataset for the time estimation. x has to be a 1D array with
        values: nbrOfLayers, nbrOfNodesPerLayer, learningRate. y has to be a single float which contains the running time
        measurement for one model in seconds."""
        np.savetxt('estTimeData.csv', [x,y], delimiter=',')

    def saveTimeMeasurementData(self, hyperParamsObjList, timeMeasurement):
        # Prepare data (convert hyperParamsList to Array with 3 cols (nbrOfLayers, nbrOfNodesPerLayer, leraning Rate)
        hyperParamsData = self.hyperParamsListToData(hyperParamsObjList)
        # Get old data
        (x,y) = self.getEstTimeData()

        print(x)
        print(y)

        # Append new data to old data
        xNew = np.append(x, hyperParamsData, axis = 0)
        yNew = np.append(y, timeMeasurement)

        newDataToWrite = np.column_stack((xNew, yNew))

        # Save data to csv
        np.savetxt('estTimeData.csv', newDataToWrite, delimiter=',')

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
        p1 = ProjectModel("FakeProject 1")
        p2 = ProjectModel("FakeProject 2")
        p3 = ProjectModel("FakeProject 3")
        return list(p1, p2, p3)

    def saveProjectList(self):
        print("Empty method: SaverLoader.saveProjectList")
