from src.hyperOptimizeApp.persistence.DatabaseConnector import DatabaseConnector
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel


class ProjectInteractionModel:
    def __init__(self):
        self.projectDB = DatabaseConnector()

    def getProjectList(self):
        projectList = self.projectDB.getAllProjects()
        return projectList

    def getProjectById(self, projectId=int):
        return self.projectDB.getProjectById(projectId)

    def deleteProjectById(self, projectId):
        self.projectDB.deleteProjectById(projectId)

    def saveProject(self, project=DatabaseProjectModel):
        projectId = self.projectDB.addProject(project.projectName)
        project.projectId = projectId
        return project

    def saveProjectById(self, project=DatabaseProjectModel):
        self.projectDB.updateProject(project)
