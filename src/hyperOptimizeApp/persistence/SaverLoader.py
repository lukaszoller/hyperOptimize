import numpy as np

class SaverLoader:
    def __init__(self):
        pass

    def getEstTimeData(self):

        fileName = 'resources/estTimeData.csv'
        try:
            data = np.genfromtxt(fileName, delimiter=',', skip_header=True)
            print("SaverLoader: data loaded successfully.")
            y = data[:,-1]
            x = data[:,0:len(data[1,:])-1]
            return x, y
        except IOError:
            print("Error. Could not read file:", fileName)
