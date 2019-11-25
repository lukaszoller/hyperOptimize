import tkinter as tk
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel


class TrainModelView(tk.Frame):
    controlFrame = None
    databaseModel = None
    model = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="blue")
        self.place(relx=0, rely=0, height=height, width=width)

        rowCount = 0

        # Text on opening window
        welcomeText = tk.Label(self, text='Here you can optimize a Model \n'
                                          'Please consider checking the time to execute').grid(row=rowCount, column=3)
        rowCount += 1

        # ROW 2
        trainModelButton = tk.Button(self, text='Optimize', command=lambda: self.checkTimeAndOptimize()).grid(row=rowCount, column=3)
        rowCount += 1

    def setModel(self, model=DatabaseModelModel):
        self.databaseModel = model
    
    def addControlFrame(self, frame):
        self.controlFrame = frame

    def checkTimeAndOptimize(self):
        pass

