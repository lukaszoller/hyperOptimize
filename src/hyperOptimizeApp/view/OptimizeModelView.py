import tkinter as tk
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj


class OptimizeModelView(tk.Frame):
    controlFrame = None
    databaseModel = None
    model = None
    range = RangeForHyperParamsObj()

    # Constants:
    MAX_LAYERS = RangeForHyperParamsObj.MAX_NUMBER_OF_HIDDEN_LAYERS

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="blue")
        self.place(relx=0, rely=0, height=height, width=width)

        rowCount = 0

        # Text on opening window
        welcomeText = tk.Label(self, text='Here you can optimize a Model \n'
                                          'Please consider checking the time to execute').grid(row=rowCount, column=2)
        rowCount += 1

        # Row with sliders for choosing number of Layers
        self.minLayerSliderValue = tk.IntVar()
        self.minLayerSliderValue.set(2)
        self.maxNodeSliderValue = tk.IntVar()
        self.maxNodeSliderValue.set(100)

        layerText = tk.Label(self, text='Range of Layers to test').grid(row=rowCount, column=1)
        self.layerSliderMin = tk.Scale(self, from_=2, to=self.MAX_LAYERS, orient=tk.HORIZONTAL, label='Min:',
                                       command=lambda x: self.setMinLayerValue(x)).grid(row=rowCount, column=2)
        self.layerSliderMax = tk.Scale(self, from_=2, to=self.MAX_LAYERS, orient=tk.HORIZONTAL,
                                       label='Max:', command=lambda x: self.setMaxNodeValue(x))
        self.layerSliderMax.set(self.MAX_LAYERS)
        self.layerSliderMax.grid(row=rowCount, column=3)
        rowCount += 1

        # Row with sliders for choosing number of Nodes per Layer
        self.minNodeSliderValue = tk.IntVar()
        self.minNodeSliderValue.set(1)
        nodeText = tk.Label(self, text='Range of Nodes\nper layer to test').grid(row=rowCount, column=1)
        self.nodeSliderMin = tk.Scale(self, from_=1, to=self.MAX_LAYERS, orient=tk.HORIZONTAL, label='Min: ',
                                      command=lambda x: self.setMinNodeValue(x))
        self.nodeSliderMin.grid(row=rowCount, column=2)
        self.nodeSliderMax = tk.Scale(self, from_=1, to=self.MAX_LAYERS, orient=tk.HORIZONTAL,
                                      label='Max: ')
        self.nodeSliderMax.set(self.MAX_LAYERS)
        self.nodeSliderMax.grid(row=rowCount, column=3)
        rowCount += 1

        # Final Row (Train Model)
        trainModelButton = tk.Button(self, text='Optimize', command=lambda: self.checkTimeAndOptimize()).grid(
            row=rowCount, column=3)
        rowCount += 1

    def setModel(self, model=DatabaseModelModel):
        self.databaseModel = model

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def checkTimeAndOptimize(self):
        pass

    def setMinLayerValue(self, number):
        self.minLayerSliderValue.set(number)
        self.layerSliderMax.configure(from_=self.minLayerSliderValue.get())

    def setMinNodeValue(self, number):
        self.minNodeSliderValue.set(number)
        self.nodeSliderMax.configure(from_=self.minNodeSliderValue.get())

    def setMaxNodeValue(self, number):
        self.maxNodeSliderValue.set(number)
        self.nodeSliderMin.configure(to=self.maxNodeSliderValue.get())
        self.nodeSliderMax.configure(to=self.maxNodeSliderValue.get())
