import tkinter as tk
from src.hyperOptimizeApp.logic.dbInteraction.ModelInteractionModel import ModelInteractionModel
from src.hyperOptimizeApp.logic.viewInteraction.ModelModel import ModelModel
from src.hyperOptimizeApp.logic.dbInteraction.ProjectInteractionModel import ProjectInteractionModel
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel


class ModelView(tk.Frame):
    model = ModelModel()
    controlFrame = None
    project = DatabaseProjectModel()

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="blue")
        self.place(relx=0, rely=0, height=height, width=width)
        self.topText = tk.StringVar()
        self.topText.set("Model")

        rowCount = 0

        # ROW 1
        topLabel = tk.Label(self, textvariable=self.topText).grid(row=rowCount, column=3)
        rowCount += 1

    def setProject(self, project=DatabaseProjectModel()):
        self.project = project

    def setModel(self, model=ModelModel):
        self.model = model

    def setTopText(self, text):
        self.topText.set(text)

    def addControlFrame(self, frame):
        self.controlFrame = frame
