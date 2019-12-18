from src.hyperOptimizeApp.persistence.dbInteraction.ProjectInteractionModel import ProjectInteractionModel


class HomeModel:
    def __init__(self):
        self.projectInteract = ProjectInteractionModel()

    def getProjectList(self):
        return self.projectInteract.getProjectList()
