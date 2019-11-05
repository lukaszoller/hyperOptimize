from src.hyperOptimizeApp.persistence.ProjectDatabase import ProjectDatabase


class ProjectInteractionModel:
    def __init__(self, projectDB=ProjectDatabase):
        self.projectDB = ProjectDatabase()

    def getProjectList(self):
        projectList = self.projectDB.getAllProjects()
        return projectList

    def getProjectById(self, projectId=int):
        return self.projectDB.getProjectById(projectId)