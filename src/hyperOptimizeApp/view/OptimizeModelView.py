import tkinter as tk
import tkinter.messagebox
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.dbInteraction.DataInteractionModel import DataInteractionModel
from src.hyperOptimizeApp.logic.dbInteraction.ModelInteractionModel import ModelInteractionModel
from src.hyperOptimizeApp.view.tools.Tooltip import CreateToolTip as tt
from src.hyperOptimizeApp.view.tools.RangeSlider import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
from src.hyperOptimizeApp.view.tools import LayoutConstants



class OptimizeModelView(tk.Frame):
    estimateTimeAlreadyShowed = False  # needed to decide if optimize button should execute optimize function
    # without showing running time estimation warning
    dataInteraction = DataInteractionModel()
    modelInteraction = ModelInteractionModel()
    controlFrame = None
    model = None
    rangeForHyperParamsObj = None
    optimizeParamsModel = None
    project = None
    loadDataModel = None

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
        self.layerSlider = RangeSlider(self, text='minmax', lowerBound=2, upperBound=self.MAX_LAYERS,
                                       initialLowerBound=2, initialUpperBound=50,
                                       orient=tk.HORIZONTAL,
                                       command=lambda x, y: self.setMaxNodeValue(y), sliderColor="yellow",
                                       sliderHighlightedColor="green", barColor="lightblue", setLowerBound=True,
                                       setUpperBound=True,
                                       caretColor="red", caretHighlightedColor="green",
                                       barWidthPercent=0.85, barHeightPercent=0.2)
        self.layerSlider.grid(row=rowCount, column=2, columnspan=2)
        self.layerSlider.setMinorTickSpacing(1)
        self.layerSlider.setSnapToTicks(True)

        layerHelp = tk.Label(self, text='?')
        layerHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with sliders for choosing number of Nodes per Layer
        nodeText = tk.Label(self, text='Range of Nodes\nper layer to test').grid(row=rowCount, column=1)
        self.nodeSlider = RangeSlider(self, text='minmax', lowerBound=2, upperBound=self.MAX_LAYERS,
                                      initialLowerBound=2, initialUpperBound=50,
                                      sliderColor="yellow", setLowerBound=True, setUpperBound=True,
                                      sliderHighlightedColor="green", barColor="lightblue",
                                      caretColor="red", caretHighlightedColor="green",
                                      barWidthPercent=0.85, barHeightPercent=0.2)
        self.nodeSlider.grid(row=rowCount, column=2, columnspan=2)
        self.nodeSlider.setMinorTickSpacing(1)
        self.nodeSlider.setSnapToTicks(True)
        nodeHelp = tk.Label(self, text='?')
        nodeHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with slider für Dropout
        dropoutText = tk.Label(self, text='Percentage of nodes weights set to 0').grid(row=rowCount, column=1)
        self.dropoutSlider = tk.Scale(self, from_=0.01, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        self.dropoutSlider.grid(row=rowCount, column=2, padx=5, pady=3)
        dropoutHelp = tk.Label(self, text='?')
        dropoutHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with picking of different activation Functions
        self.activationCheckBtnVarDict = dict()
        ## Sigmoid
        sigmoidBoxName = "Sigmoid Function"
        activationText = tk.Label(self, text='Activation functions to choose').grid(row=rowCount, column=1)
        self.sigmoidVar = tk.IntVar(0)
        sigmoidBox = tk.Checkbutton(self, text=sigmoidBoxName, variable=self.sigmoidVar)
        sigmoidBox.grid(row=rowCount, column=2)
        self.activationCheckBtnVarDict['sigmoid'] = self.sigmoidVar
        ## Linear
        linearBoxName = "Linear Function"
        self.linearVar = tk.IntVar(0)
        linearBox = tk.Checkbutton(self, text=linearBoxName, variable=self.linearVar)
        linearBox.grid(row=rowCount, column=3)
        self.activationCheckBtnVarDict['linear'] = self.linearVar
        rowCount += 1
        ## Tanh
        tanhBoxName = "Tanh Function"
        self.tanhVar = tk.IntVar(0)
        tanhBox = tk.Checkbutton(self, text=tanhBoxName, variable=self.tanhVar)
        tanhBox.grid(row=rowCount, column=2)
        self.activationCheckBtnVarDict['tanh'] = self.tanhVar
        ## Relu
        reluBoxName = "ReLu Function"
        self.reluVar = tk.IntVar(0)
        reluBox = tk.Checkbutton(self, text=reluBoxName, variable=self.reluVar)
        reluBox.grid(row=rowCount, column=3)
        self.activationCheckBtnVarDict['relu'] = self.reluVar
        activationHelp = tk.Label(self, text='?')
        activationHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Row with slider für nbrOfModels
        nbrOfModelsText = tk.Label(self, text='Number of models').grid(row=rowCount, column=1)
        self.nbrOfModelsSlider = tk.Scale(self, from_=2, to=200, orient=tk.HORIZONTAL, resolution=1)
        self.nbrOfModelsSlider.grid(row=rowCount, column=2, padx=5, pady=3)
        nbrOfModelsHelp = tk.Label(self, text='?')
        nbrOfModelsHelp.grid(row=rowCount, column=4)
        rowCount += 1

        # Final Row (Train Model)
        trainModelButton = tk.Button(self, text='Optimize', command=lambda: self.checkAndOptimize()).grid(
            row=rowCount, column=3)
        estTimeButton = tk.Button(self, text='Estimate running time', command=lambda: self.showTimeEstimateInformation()).grid(
            row=rowCount, column=4)

        rowCount += 1

        # TOOLTIPS ---------------
        layerTooltip = tt(layerHelp, 'Tooltip for Layers')
        nodeTooltip = tt(nodeHelp, 'Tooltip for Nodes')
        dropoutTooltip = tt(dropoutHelp, 'Tooltip for dropout percentage')
        activationTooltip = tt(activationHelp, 'Tooltip for activation function')
        nbrOfModelsTooltip = tt(nbrOfModelsHelp, 'Number of models which are picked randomly from specified range.')
        rowCount += 1

        # TOOLTIPS ---------------

        # Optimization process information
        # Todo: change layout with frames and enable the following code.
        # optimizationInfoFrame = tk.Frame(self)
        # optimizationInfoFrame.pack(fill=tk.X)
        # self. optimizationInfoLabel = tk.Label(optimizationInfoFrame, text="", width=50)
        # self. optimizationInfoLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

    def setModel(self, model):
        self.model = model

    def setProject(self, project):
        self.project = project

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def checkAndOptimize(self):
        print("OptimizeModelView.checkAndOptimize executed")
        # Check if at least one activation function has been chosen
        if not self.checkActivation():
            tk.messagebox.showwarning("Activation Error", "Please select at least one activation function!")
        # Check if data has been loaded
        elif self.loadDataModel.data == None:
            tk.messagebox.showwarning("Data Error", "No data has been loaded to project. Load data before optimizing.")
        else:
            # if not existent, create optimizeParamsModel (this has to be optional because self.estimateTime needs it too
            # and its not clear if this function or self.estimateTime is executed first.
            self.createOptimizeParamsModel()  # this line exists two times, second one in self.estimateTime it
            # runs optionally.

            # Check running time estimation
            stringTime, timeInSeconds = self.estimateTime()
            if timeInSeconds > 3600:
                answer = self.showTimeEstimateWarning()
                if answer:  # User clicks on "Yes continue with evaluation"
                    self.optimizeParamsModel.evaluateModels()
                else:
                    return  # Stop execution if User clicks on "No"

            self.optimizeParamsModel.evaluateModels()

            # ToDo: after best model is computed change back to model view and display modelparams in corresponding fields.
            bestModel = self.optimizeParamsModel.getBestModel()
            print("Best Model evaluated:", bestModel)

            # Update model with optimized params
            self.modelInteraction.updateModelParams(self.model, bestModel)
            self.model = self.modelInteraction.getModelById(self.model.modelId)

            # Pop up asking for results to show
            self.askShowResults()

    def askShowResults(self):
        answer = tk.messagebox.askyesno("Show Results?", "Optimal Model found.\n"
                                                         "Do you want to see the result graph?")
        if answer == 1:
            self.showResultsPlot()
            self.controlFrame.setModelFrameWithParameters(self.model, self.project)
        else:
            self.controlFrame.setModelFrameWithParameters(self.model, self.project)

    def showResultsPlot(self):
        newWindow = tk.Toplevel(self)

        # plot
        # figure = plt.Figure(figsize=(6, 5), dpi=100)
        figure = self.optimizeParamsModel.getFigureTest()
        plot = FigureCanvasTkAgg(figure, newWindow)
        plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        newWindow.mainloop()


    def setMaxNodeValue(self, number):
        self.maxNodeSliderValue.set(number)
        self.nodeSlider.configure(to=self.maxNodeSliderValue.get())


    def checkActivation(self):
        # Check if an activation function is set
        if (self.sigmoidVar.get() == 0) & (self.linearVar.get() == 0) & \
                (self.tanhVar.get() == 0) & (self.reluVar.get() == 0):
            return False
        return True

    def estimateTime(self):
        """Creates the OptimizeParamsModel-Object, if not already existent (because some information from this object
        is needed for the estimation. Returns the time estimate (stringTime, timeInSeconds)."""
        # if not existent, create optimizeParamsModel (this has to be optional because self.checkAndOptimize() needs it too
        # and its not clear if this function or self.estimateTime is executed first.
        self.createOptimizeParamsModel()  # this line exists two times, second one in self.checkAndOptimize. It runs
        # optionally.
        etm = EstimateTimeModel()
        timeEstimate = etm.estimateTime(self.optimizeParamsModel.hyperParamsObjList)
        return timeEstimate

    def showTimeEstimateInformation(self):
        stringTime, timeInSeconds = self.estimateTime()
        message = "The optimization will take approximately " + stringTime + "[hh:mm:ss]."
        tk.messagebox.showinfo("Running time estimation", message)

    def showTimeEstimateWarning(self):
        stringTime, timeInSeconds = self.estimateTime()
        message = "Attention! The optimization will take approximately " + stringTime + "[hh:mm:ss].\nDo " \
                                                                                        "you want to continue?"
        msgBox = tk.messagebox.askquestion("Warning: long running time", message, icon='warning')
        if msgBox == 'yes':
            return True
        else:
            return False

    def optimizationMessageSuccess(self):
        self.optimizationInfoLabel.config(text="Optimization successfull!", fg="green")

    def optimizationMessageFailure(self):
        self.optimizationInfoLabel.config(text="Warning! Optimization failed!", fg="red")

    def createRangeForHyperParamsObj(self):
        """Takes information from GUI and creates a RangeForHyperParamsobj."""
        # Get hyperparam ranges
        minNbrOfNodes = int(self.nodeSlider.getLower())
        maxNbrOfNodes = int(self.nodeSlider.getUpper())
        minNbrOfLayers = int(self.layerSlider.getLower())
        maxNbrOfLayers = int(self.layerSlider.getUpper())
        minDropout = int(self.dropoutSlider.get() * 100)
        maxDropout = int(self.dropoutSlider.get() * 100)
        activationArray = self.getActivationCheckBtnValues()
        nbrOfCategories = self.loadDataModel.nbrOfCategories
        # explanation of next line: shape of 3rd dataset (=[2]) of loadDataModel (=rawData), [1]=colnumbers)
        nbrOfFeatures = np.shape(self.loadDataModel.data[2])[1]-nbrOfCategories
        print("Min Number of Nodes: " + str(minNbrOfNodes))
        print("Max Number of Nodes: " + str(maxNbrOfNodes))
        print("Min Number of Layers: " + str(minNbrOfLayers))
        print("Max Number of Layers: " + str(maxNbrOfLayers))
        print("Min Number of Dropout: " + str(minDropout))
        print("Max Number of Dropout: " + str(maxDropout))
        print("Activation Array: " + str(activationArray))
        # activationArray = np.array(['sigmoid', 'elu', 'softmax'])

        self.rangeForHyperParamsObj = RangeForHyperParamsObj()
        self.rangeForHyperParamsObj.nbrOfHiddenLayersDict = dict({'min': minNbrOfLayers, 'max': maxNbrOfLayers})
        self.rangeForHyperParamsObj.nbrOfHiddenUnitsDict = dict({'min': minNbrOfNodes, 'max': maxNbrOfNodes})
        self.rangeForHyperParamsObj.dropOutDict = dict({'min': minDropout, 'max': maxDropout})
        self.rangeForHyperParamsObj.activationArray = activationArray
        self.rangeForHyperParamsObj.nbrOfCategories = nbrOfCategories
        self.rangeForHyperParamsObj.nbrOfFeatures = nbrOfFeatures

    def setProject(self, project):
        self.project = project
        self.loadDataModel = self.dataInteraction.getLoadDataModel(self.project.projectId)
        self.loadDataModel.dataIsForTraining = True
        self.loadDataModel.loadData()

    def getActivationCheckBtnValues(self):
        """Gets values from checkbuttons for activation functions and returns an array in the form the optimizing
        function requires."""
        activationFunctionArray = []

        for key, var in self.activationCheckBtnVarDict.items():
            if var.get() == 1:
                activationFunctionArray.append(key)

        return activationFunctionArray

    def createOptimizeParamsModel(self):
        """The creation of the optimizeParamsModel is placed in a separate function because this object is needed from
        two functions (self.estimateTime and self.checkAndOptimize). But it is not clear, which function will be
        executed first."""
        # if self.optimizeParamsModel is None:          todo: most probably not needed. delete if everything works
        self.createRangeForHyperParamsObj()
        nbrOfModels = int(self.nbrOfModelsSlider.get())
        x_train, y_train, x_test, y_test = self.getTrainTestData()
        self.optimizeParamsModel = OptimizeParamsModel(x_train, y_train, x_test, y_test, self.rangeForHyperParamsObj,
                                                           nbrOfModels)

    # def getHyperParamsObject(self):
    #     return self.model.hyperParamsObj

    def getTrainTestData(self):
        """Get the whole data and splits it into training and testing set."""
        # get whole dataset
        x, y, rawData = self.loadDataModel.data

        # split dataset
        l = len(x[:, 0])  # rownumber of whole dataset
        trainRowNumber = self.loadDataModel.trainRowNumber

        x_train = x[0:trainRowNumber, :]
        y_train = y[0:trainRowNumber, :]
        x_test = x[trainRowNumber:l, :]
        y_test = y[trainRowNumber:l, :]

        return x_train, y_train, x_test, y_test
