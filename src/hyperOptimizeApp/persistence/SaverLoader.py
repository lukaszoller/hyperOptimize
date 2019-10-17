from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel
import numpy as np

class SaverLoader:
    def __init__(self):
        pass

    def getEstTimeData(self):
        """ Returns two arrays. A 2D array x and a 1D array y."""
        fileName = 'estTimeData.csv'
        try:
            data = np.genfromtxt(fileName, delimiter=',', skip_header=True)
            print("SaverLoader: data loaded successfully.")
            y = data[:,-1]
            x = data[:,0:len(data[1,:])-1]
            return x, y
        except IOError:
            print("Error. Could not read file:", fileName)

    def saveTimeMeasurementData(self, x, y):
        """Appends a new time measurement to the training dataset for the time estimation. x has to be a 1D array with
        values: nbrOfLayers, nbrOfNodesPerLayer, learningRate. y has to be a single float which contains the running time
        measurement for one model in seconds."""
        np.savetxt('estTimeData.csv', [x,y], delimiter=',')

    def getProjectList(self):
        p1 = ProjectModel("FakeProject 1")
        p2 = ProjectModel("FakeProject 2")
        p3 = ProjectModel("FakeProject 3")
        return list(p1, p2, p3)

    def saveProjectList(self):
        print("Empty method: SaverLoader.saveProjectList")
