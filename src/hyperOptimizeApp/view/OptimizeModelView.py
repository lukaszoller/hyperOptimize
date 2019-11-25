import tkinter as tk
import tkinter.messagebox
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.viewInteraction.Tooltip import CreateToolTip as tt


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
        self.layerSliderMax.grid(row=rowCount, column=3, padx=5, pady=3)
        layerHelp = tk.Label(self, text='?')
        layerHelp.grid(row=rowCount, column=4)
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
        self.nodeSliderMax.grid(row=rowCount, column=3, padx=5, pady=3)
        nodeHelp = tk.Label(self, text='?')
        nodeHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with slider für Dropout
        dropoutText = tk.Label(self, text='Percentage of nodes weights set to 0').grid(row=rowCount, column=1)
        self.dropoutSlider = tk.Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01).\
            grid(row=rowCount, column=2, padx=5, pady=3)
        dropoutHelp = tk.Label(self, text='?')
        dropoutHelp.grid(row=rowCount, column=4)
        rowCount += 1

        #Row with picking of different activation Functions
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

    def checkActivation(self):
        # Check if an activation function is set
        print(self.sigmoidVar.get())
        print(self.gaussianVar.get())
        print(self.thirdVar.get())
        print(self.fourthVar.get())
        if (self.sigmoidVar.get() == 0) & (self.gaussianVar.get() == 0) & \
                (self.thirdVar.get() == 0) & (self.fourthVar.get() == 0):
            return False
        return True

    def checkTime(self):
        pass
