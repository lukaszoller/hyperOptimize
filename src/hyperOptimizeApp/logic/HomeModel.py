from src.hyperOptimizeApp.logic.ProjectInteractionModel import ProjectInteractionModel
from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel


class HomeModel:
    def __init__(self, interactionModel=ProjectInteractionModel):
        self.projectInteract = ProjectInteractionModel()
        self.projectList = self.projectInteract.getProjectList()

    def getProjectList(self):
        return self.projectList
