from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel
import numpy as np

class SaverLoader:
    def __init__(self):
        pass

    def getEstTimeData(self):
        """ Returns to arrays. A 2D array x and a 1D array y."""
        fileName = 'resources/estTimeData.csv'
        try:
            data = np.genfromtxt(fileName, delimiter=',', skip_header=True)
            print("SaverLoader: data loaded successfully.")
            y = data[:,-1]
            x = data[:,0:len(data[1,:])-1]
            return x, y
        except IOError:
            print("Error. Could not read file:", fileName)

    def saveTimeMeasurementData(self, x, y):
        np.savetxt('estTimeData.csv', [x,y], delimiter=',')

    def getProjectList(self):
        p1 = ProjectModel("FakeProject 1")
        p2 = ProjectModel("FakeProject 2")
        p3 = ProjectModel("FakeProject 3")
        return list(p1, p2, p3)

    def saveProjectList(self):
        print("Empty method: SaverLoader.saveProjectList")
