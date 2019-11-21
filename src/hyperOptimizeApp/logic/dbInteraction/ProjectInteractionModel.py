from src.hyperOptimizeApp.persistence.DatabaseConnector import ProjectDatabase


class ProjectInteractionModel:
    def __init__(self, projectDB=ProjectDatabase):
        self.projectDB = ProjectDatabase()

    def getProjectList(self):
        projectList = self.projectDB.getAllProjects()
        return projectList

    def getProjectById(self, projectId=int):
        return self.projectDB.getProjectById(projectId)

    def deleteProjectById(self, projectId):
        self.projectDB.deleteProjectById(projectId)
