from src.hyperOptimizeApp.logic.dbInteraction.ProjectInteractionModel import ProjectInteractionModel


class HomeModel:
    def __init__(self):
        self.projectInteract = ProjectInteractionModel()
        self.projectList = self.projectInteract.getProjectList()

    def getProjectList(self):
        return self.projectList
