import tkinter as tk
from src.hyperOptimizeApp.logic.dbInteraction.ModelInteractionModel import ModelInteractionModel
from src.hyperOptimizeApp.logic.viewInteraction.ModelModel import ModelModel
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel


class ModelView(tk.Frame):
    model = DatabaseModelModel()
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

        # ROW 2
        trainModelButton = tk.Button(self, text='Train Model', command=lambda: self.controlFrame.setTrainModelFrame(
            self.model.modelObject)).grid(row=rowCount, column=3)
        rowCount += 1

    def setProject(self, project=DatabaseProjectModel()):
        self.project = project

    def setModel(self, model=DatabaseModelModel()):
        self.model = model

    def setTopText(self, text):
        self.topText.set(text)

    def addControlFrame(self, frame):
        self.controlFrame = frame
