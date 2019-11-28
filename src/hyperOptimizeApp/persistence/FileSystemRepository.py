from src.hyperOptimizeApp.persistence.DatabaseConnector import DatabaseConnector
import numpy as np
import pandas as pd
import cpuinfo


class FileSystemRepository:

    def loadDataForTrainingOrPrediction(self, pathToData, firstRowIsHeader, firstColIsRownbr, nbrOfCategories=0,
                                        dataIsForTraining=False):
        """Loads data from filesystem. Takes as input pathToData (String representing full path to csv file),
        nbrOfFeatures (Size of X for training and prediction of model), firstRowIsHeader and firstColIsRownbr (both
        boolean Values).
        If nbrOfCategories is not 0 and dataIsForTraining = False, it will print an informational message to the console
        but will set nbrOfCategories to the value 0.
        Rownames will be removed for all outputs.
        If dataIsForTraining = True: Returns three np-arrays x (features of dataset), y (categories of dataset) and
        rawData (x and y in one array with header and without colnbrs (if they existed in the first place)).
        If dataIsForTraining = False: Returns only two arrays: x and rawData."""

        # check if nbrOfCategories = 0 if dataIsForTraining = false.
        if not dataIsForTraining and nbrOfCategories != 0:
            nbrOfCategories = 0
            print(
                "If data is used for prediction, nbrOfCategories has to be 0. Value of nbrOfCategories has been set to "
                "0 automatically.")

        # get data
        try:
            data = np.genfromtxt(pathToData, delimiter=',', skip_header=False)
            return
        except IOError:
            print("IOError: Could not read file: ", pathToData)

        # get dataset info
        nbrOfRows, nbrOfCols = np.shape(data)
        nbrOfFeatures = nbrOfCols - nbrOfCategories
        # return error if nbrOfFeatures is bigger than nbrOfcols
        if nbrOfFeatures > nbrOfCols:
            raise ValueError(
                "nbrOfFeatures is bigger than nbrOfCols in dataset. nbrOfFeatures should be smaller.Probably "
                "parameter nbrOfCategories is set wrongly.")
        # return error if nbrOfFeatures is equal to nbrOfColumns but dataset is for training (y needed)
        if nbrOfFeatures == nbrOfCols and dataIsForTraining:
            raise ValueError(
                "nbrOfFeatures has to be smaller than nbrOfCols in dataset. Probably parameter nbrOfCategories "
                "is set wrongly.")
        # Store data before manipulation
        rawData = data

        # Delete first row if it is header
        if firstRowIsHeader:
            data = data[1:nbrOfRows, :]
        # Delete first col if it is colnbr, also for rawData
        if firstColIsRownbr:
            data = data[:, 1:nbrOfCols]
            rawData = rawData[:, 1:nbrOfCols]

        x = data[:, 0:nbrOfFeatures]

        # return data
        if dataIsForTraining:
            y = data[:, nbrOfFeatures:nbrOfCols]
            return x, y, rawData
        else:
            return x, rawData

    def hoi(self):
        print("hoi")