class DatabaseProjectModel:

    # Creation of new project
    projectId = 0
    projectName = ""

    # Loading old project
    def __init__(self, projectId=0, projectName="", dataPath=None, dataIsSet=False):
        self.projectId = projectId
        self.projectName = projectName
        self.dataPath = dataPath
        self.dataIsSet = dataIsSet

    def __str__(self):
        return self.projectName

    def loadModel(self):
        pass

    def createNewProject(self):
        pass

    def setProjectName(self, name=str):
        self.projectName = name

    def getProjectName(self):
        return self.projectName

    def setProjectId(self, projectId=int):
        self.projectId = projectId

    def getProjectId(self):
        return self.projectId

    def setDataInformation(self, information):
        self.dataInformation = information

    def getDataInformation(self):
        return self.dataInformation

    def setDataPath(self, path):
        self.dataPath = path

    def getDataPath(self):
        return self.dataPath
