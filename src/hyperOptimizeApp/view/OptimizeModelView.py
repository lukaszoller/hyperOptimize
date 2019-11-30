import tkinter as tk
import tkinter.messagebox
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.viewInteraction.Tooltip import CreateToolTip as tt
from src.hyperOptimizeApp.logic.viewInteraction.RangeSlider import *


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
                                          'Please consider checking the time to execute').grid(row=rowCount, column=1)
        rowCount += 1

        # Row with sliders for choosing number of Layers
        self.maxNodeSliderValue = tk.IntVar()
        self.maxNodeSliderValue.set(100)

        layerText = tk.Label(self, text='Range of Layers to test').grid(row=rowCount, column=1)
        self.layerSlider = RangeSlider(self, label='minmax', from_=2, to=self.MAX_LAYERS, orient=tk.HORIZONTAL,
                                       command=lambda x, y: self.setMaxNodeValue(y), sliderColor="yellow",
                                       sliderHighlightedColor="green", barColor="lightblue", setLowerBound=True,
                                       setUpperBound=True,
                                       caretColor="red", caretHighlightedColor="green",
                                       barWidthPercent=0.85, barHeightPercent=0.2)
        self.layerSlider.grid(row=rowCount, column=2, columnspan=2)

        layerHelp = tk.Label(self, text='?')
        layerHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with sliders for choosing number of Nodes per Layer
        nodeText = tk.Label(self, text='Range of Nodes\nper layer to test').grid(row=rowCount, column=1)
        self.nodeSlider = RangeSlider(self, label='minmax', from_=2, to=self.MAX_LAYERS, orient=tk.HORIZONTAL,
                                      sliderColor="yellow", setLowerBound=True, setUpperBound=True,
                                      sliderHighlightedColor="green", barColor="lightblue",
                                      caretColor="red", caretHighlightedColor="green",
                                      barWidthPercent=0.85, barHeightPercent=0.2)
        self.nodeSlider.grid(row=rowCount, column=2, columnspan=2)
        nodeHelp = tk.Label(self, text='?')
        nodeHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with slider für Dropout
        dropoutText = tk.Label(self, text='Percentage of nodes weights set to 0').grid(row=rowCount, column=1)
        self.dropoutSlider = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01). \
            grid(row=rowCount, column=2, padx=5, pady=3)
        dropoutHelp = tk.Label(self, text='?')
        dropoutHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with picking of different activation Functions
        activationText = tk.Label(self, text='Activation functions to choose').grid(row=rowCount, column=1)
        self.sigmoidVar = tk.IntVar(0)
        sigmoidBox = tk.Checkbutton(self, text='Sigmoid Function', variable=self.sigmoidVar)
        sigmoidBox.grid(row=rowCount, column=2)
        self.gaussianVar = tk.IntVar(0)
        gaussianBox = tk.Checkbutton(self, text='Gaussian Function', variable=self.gaussianVar)
        gaussianBox.grid(row=rowCount, column=3)
        rowCount += 1
        self.thirdVar = tk.IntVar(0)
        thirdBox = tk.Checkbutton(self, text='Third Function', variable=self.thirdVar)
        thirdBox.grid(row=rowCount, column=2)
        self.fourthVar = tk.IntVar(0)
        fourthBox = tk.Checkbutton(self, text='Fourth Function', variable=self.fourthVar)
        fourthBox.grid(row=rowCount, column=3)
        activationHelp = tk.Label(self, text='?')
        activationHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Final Row (Train Model)
        trainModelButton = tk.Button(self, text='Optimize', command=lambda: self.checkAndOptimize()).grid(
            row=rowCount, column=3)
        rowCount += 1

        # TOOLTIPS ---------------
        layerTooltip = tt(layerHelp, 'Tooltip for Layers')
        nodeTooltip = tt(nodeHelp, 'Tooltip for Nodes')
        dropoutTooltip = tt(dropoutHelp, 'Tooltip for dropout percentage')
        activationTooltip = tt(activationHelp, 'Tooltip for activation function')
        rowCount += 1

        # TOOLTIPS ---------------

    def setModel(self, model=DatabaseModelModel):
        self.databaseModel = model

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def checkAndOptimize(self):
        if not self.checkActivation():
            tk.messagebox.showwarning("Activation Error", "Please select at least one activation function!")
        else:
            pass

    def setMaxNodeValue(self, number):
        self.maxNodeSliderValue.set(number)
        self.nodeSlider.configure(to=self.maxNodeSliderValue.get())

    def checkActivation(self):
        # Check if an activation function is set
        if (self.sigmoidVar.get() == 0) & (self.gaussianVar.get() == 0) & \
                (self.thirdVar.get() == 0) & (self.fourthVar.get() == 0):
            return False
        return True

    def checkTime(self):
        pass
