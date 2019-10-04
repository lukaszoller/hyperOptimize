from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader
from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel



class HomeModel:
    def __init__(self):
        saverLoader = SaverLoader()
        self.projectList = saverLoader.getProjectList()

    def createNewProject(self, projectName):
        self.projectList.append(ProjectModel(projectName))

    def loadProject(self, listIndex):
        return self.projectList.__getitem__(listIndex)

