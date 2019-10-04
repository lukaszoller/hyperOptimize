



class ProjectModel:

    # Creation of new project
    def __init__(self, projectName):
        self.projectName = projectName

    # Loading old project
    def __init__(self, projectName, dataInformation, modelList):
        self.projectName = projectName
        self.dataInformation = dataInformation
        self.modelList = modelList

    def __str__(self):
        return "ProjectModel.str: " + self.projectName

    def loadModel(self):
        pass

    def createNewProject(self):
        pass




