import tkinter as tk
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel


class TrainModelView(tk.Frame):
    controlFrame = None
    databaseModel = None
    model = None

    def __init__(self, main, height, width):
        tk.Frame.__init__(self, main)

        self.config(bg="blue")
        self.place(relx=0, rely=0, height=height, width=width)

    def setModel(self, model=DatabaseModelModel):
        self.databaseModel = model
    
    def addControlFrame(self, frame):
        self.controlFrame = frame
