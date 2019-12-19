import tkinter as tk
import tkinter.messagebox
from src.hyperOptimizeApp.logic.OptimizeParamsModel import OptimizeParamsModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.persistence.dbInteraction.DataInteractionModel import DataInteractionModel
from src.hyperOptimizeApp.persistence.dbInteraction.ModelInteractionModel import ModelInteractionModel
from src.hyperOptimizeApp.view.tools.Tooltip import CreateToolTip as tt
from src.hyperOptimizeApp.view.tools import ValidationFunctions
import numpy as np

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
    errorString = ""

    # Constants:
    MAX_LAYERS = RangeForHyperParamsObj.MAX_NUMBER_OF_HIDDEN_LAYERS
    MAX_NODES = RangeForHyperParamsObj.MAX_NUMBER_OF_HIDDEN_LAYERS

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)
        self.width = width

        self.place(relx=0, rely=0, height=height, width=width)

        # Text on opening window
        welcomeFrame = tk.Frame(self, width=self.width-100)
        welcomeFrame.pack(fill=tk.X)
        welcomeText = tk.Label(welcomeFrame, text='Here you can optimize a Model \n'
                                                  'Please consider checking the time to execute')
        welcomeText.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Row with sliders for choosing number of Layers
        # Todo: validation functions for correct number handling
        layerFrame = tk.Frame(self, width=self.width-100)
        layerFrame.pack(fill=tk.X)
        innerLayerFrame = tk.Frame(layerFrame, width=self.width - 110)
        innerLayerFrame.pack(fill=tk.X, side=tk.RIGHT)
        layerText = tk.Label(layerFrame, text='Range of Layers to test')
        layerText.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        self.nbrLayersValidation = (self.register(ValidationFunctions.isPositiveNumber), '%S')
        self.entryNbrMinLayers = tk.Entry(innerLayerFrame, width=10, validate="key",
                                          validatecommand=self.nbrLayersValidation)
        self.entryNbrMinLayers.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.entryNbrMaxLayers = tk.Entry(innerLayerFrame, width=10, validate="key",
                                          validatecommand=self.nbrLayersValidation)
        self.entryNbrMaxLayers.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        layerHelp = tk.Label(innerLayerFrame, text='?')
        layerHelp.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # self.layerSlider = RangeSlider(self, text='minmax', lowerBound=2, upperBound=self.MAX_LAYERS,
        #                                initialLowerBound=2, initialUpperBound=50,
        #                                orient=tk.HORIZONTAL,
        #                                command=lambda x, y: self.setMaxNodeValue(y), sliderColor="yellow",
        #                                sliderHighlightedColor="green", barColor="lightblue", setLowerBound=True,
        #                                setUpperBound=True,
        #                                caretColor="red", caretHighlightedColor="green",
        #                                barWidthPercent=0.85, barHeightPercent=0.2)
        # self.layerSlider.grid(row=rowCount, column=2, columnspan=2)
        # self.layerSlider.setMinorTickSpacing(1)
        # self.layerSlider.setSnapToTicks(True)

        # Row with sliders for choosing number of Nodes per Layer
        nodeFrame = tk.Frame(self, width=self.width-100)
        nodeFrame.pack(fill=tk.X)
        innerNodeFrame = tk.Frame(nodeFrame, width=self.width - 110)
        innerNodeFrame.pack(side=tk.RIGHT, fill=tk.X)
        nodeText = tk.Label(nodeFrame, text='Range of Nodes\nper layer to test')
        nodeText.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        self.nbrNodesValidation = self.register(ValidationFunctions.isPositiveNumber)

        self.entryNbrMinNodes = tk.Entry(innerNodeFrame, width=10, validate="key",
                                         validatecommand=(self.nbrNodesValidation, '%S'))
        self.entryNbrMinNodes.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.entryNbrMaxNodes = tk.Entry(innerNodeFrame, width=10, validate="key",
                                         validatecommand=(self.nbrNodesValidation, '%S'))
        self.entryNbrMaxNodes.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        nodeHelp = tk.Label(innerNodeFrame, text='?')
        nodeHelp.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # self.nodeSlider = RangeSlider(self, text='minmax', lowerBound=2, upperBound=self.MAX_LAYERS,
        #                               initialLowerBound=2, initialUpperBound=50,
        #                               sliderColor="yellow", setLowerBound=True, setUpperBound=True,
        #                               sliderHighlightedColor="green", barColor="lightblue",
        #                               caretColor="red", caretHighlightedColor="green",
        #                               barWidthPercent=0.85, barHeightPercent=0.2)
        # self.nodeSlider.grid(row=rowCount, column=2, columnspan=2)
        # self.nodeSlider.setMinorTickSpacing(1)
        # self.nodeSlider.setSnapToTicks(True)

        # Row with slider für Dropout
        dropoutFrame = tk.Frame(self, width=self.width-100)
        dropoutFrame.pack(fill=tk.X)
        innerDropoutFrame = tk.Frame(dropoutFrame, width=self.width - 110)
        innerDropoutFrame.pack(side=tk.RIGHT, fill=tk.X)
        dropoutText = tk.Label(dropoutFrame, text='Percentage of nodes weights set to 0\n'
                                                  'min: 1, max 99')
        dropoutText.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.nbrDropoutValidation = self.register(ValidationFunctions.isPositiveNumber)

        self.entryNbrMinDropout = tk.Entry(innerDropoutFrame, width=10, validate="key",
                                           validatecommand=(self.nbrDropoutValidation, '%S'))
        self.entryNbrMinDropout.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.entryNbrMaxDropout = tk.Entry(innerDropoutFrame, width=10, validate="key",
                                           validatecommand=(self.nbrDropoutValidation, '%S'))
        self.entryNbrMaxDropout.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        dropoutHelp = tk.Label(innerDropoutFrame, text='?')
        dropoutHelp.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # self.dropoutSlider = tk.Scale(self, from_=0.01, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        # self.dropoutSlider.grid(row=rowCount, column=2, padx=5, pady=3)

        # Row for picking Learning rate:
        learningFrame = tk.Frame(self, width=self.width-100)
        learningFrame.pack(fill=tk.X)
        innerLearningFrame = tk.Frame(learningFrame, width=self.width - 110)
        innerLearningFrame.pack(side=tk.RIGHT, fill=tk.X)
        learningText = tk.Label(learningFrame, text='Negative Log of Learning rate\n'
                                                    'min 7 for 1e-7, max 0 for 1e-0')
        learningText.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.nbrLearningValidation = self.register(ValidationFunctions.isPositiveNumber)

        self.entryNbrMinLearning = tk.Entry(innerLearningFrame, width=10, validate="key",
                                            validatecommand=(self.nbrLearningValidation, '%S'))
        self.entryNbrMinLearning.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.entryNbrMaxLearning = tk.Entry(innerLearningFrame, width=10, validate="key",
                                            validatecommand=(self.nbrLearningValidation, '%S'))
        self.entryNbrMaxLearning.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        learningHelp = tk.Label(innerLearningFrame, text='?')
        learningHelp.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # Row for picking Learning rate decay:
        learningDecayFrame = tk.Frame(self, width=self.width-100)
        learningDecayFrame.pack(fill=tk.X)
        innerLearningDecayFrame = tk.Frame(learningDecayFrame, width=self.width - 110)
        innerLearningDecayFrame.pack(side=tk.RIGHT, fill=tk.X)
        learningDecayText = tk.Label(learningDecayFrame, text='Negative Log of Learning rate decay\n'
                                                              'min 10 for 1e-10, max 1 for 1e-1')
        learningDecayText.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.nbrLearningDecayValidation = self.register(ValidationFunctions.isPositiveNumber)

        self.entryNbrMinLearningDecay = tk.Entry(innerLearningDecayFrame, width=10, validate="key",
                                                 validatecommand=(self.nbrLearningDecayValidation, '%S'))
        self.entryNbrMinLearningDecay.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.entryNbrMaxLearningDecay = tk.Entry(innerLearningDecayFrame, width=10, validate="key",
                                                 validatecommand=(self.nbrLearningDecayValidation, '%S'))
        self.entryNbrMaxLearningDecay.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        learningDecayHelp = tk.Label(innerLearningDecayFrame, text='?')
        learningDecayHelp.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # Row with picking of different activation Functions
        activationFrame = tk.Frame(self, width=self.width-100)
        activationFrame.pack(fill=tk.X)
        innerActivationFrame = tk.Frame(activationFrame, width=self.width - 110)
        innerActivationFrame.pack(side=tk.RIGHT, fill=tk.X)
        self.activationCheckBtnVarDict = dict()

        activationText = tk.Label(activationFrame, text='Activation functions to choose')
        activationText.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        ## Sigmoid
        sigmoidBoxName = "Sigmoid Function"
        self.sigmoidVar = tk.IntVar(0)
        sigmoidBox = tk.Checkbutton(innerActivationFrame, text=sigmoidBoxName, variable=self.sigmoidVar)
        sigmoidBox.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.activationCheckBtnVarDict['sigmoid'] = self.sigmoidVar

        ## Linear
        linearBoxName = "Linear Function"
        self.linearVar = tk.IntVar(0)
        linearBox = tk.Checkbutton(innerActivationFrame, text=linearBoxName, variable=self.linearVar)
        linearBox.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.activationCheckBtnVarDict['linear'] = self.linearVar

        ## Tanh
        tanhBoxName = "Tanh Function"
        self.tanhVar = tk.IntVar(0)
        tanhBox = tk.Checkbutton(innerActivationFrame, text=tanhBoxName, variable=self.tanhVar)
        tanhBox.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.activationCheckBtnVarDict['tanh'] = self.tanhVar

        ## elu
        eluBoxName = "eLu Function"
        self.eluVar = tk.IntVar(0)
        eluBox = tk.Checkbutton(innerActivationFrame, text=eluBoxName, variable=self.eluVar)
        eluBox.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.activationCheckBtnVarDict['elu'] = self.eluVar

        ## SoftMax
        softmaxBoxName = "SoftMax Function"
        self.softmaxVar = tk.IntVar(0)
        softmaxBox = tk.Checkbutton(innerActivationFrame, text=softmaxBoxName, variable=self.softmaxVar)
        softmaxBox.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.activationCheckBtnVarDict['softmax'] = self.softmaxVar

        ## Relu
        reluBoxName = "ReLu Function"
        self.reluVar = tk.IntVar(0)
        reluBox = tk.Checkbutton(innerActivationFrame, text=reluBoxName, variable=self.reluVar)
        reluBox.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.activationCheckBtnVarDict['relu'] = self.reluVar

        activationHelp = tk.Label(innerActivationFrame, text='?')
        activationHelp.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # Row with slider für nbrOfModels
        nbrOfModelsFrame = tk.Frame(self, width=self.width-100)
        nbrOfModelsFrame.pack(fill=tk.X)
        innerNbrOfModelsFrame = tk.Frame(nbrOfModelsFrame, width=self.width - 110)
        innerNbrOfModelsFrame.pack(side=tk.RIGHT, fill=tk.X)
        nbrOfModelsText = tk.Label(nbrOfModelsFrame, text='Number of models')
        nbrOfModelsText.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.nbrOfModelsSlider = tk.Scale(innerNbrOfModelsFrame, from_=2, to=100, orient=tk.HORIZONTAL, resolution=1)
        self.nbrOfModelsSlider.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        nbrOfModelsHelp = tk.Label(innerNbrOfModelsFrame, text='?')
        nbrOfModelsHelp.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # Final Row (Train Model)
        trainFrame = tk.Frame(self, width=self.width-100)
        trainFrame.pack(fill=tk.X)
        trainModelButton = tk.Button(trainFrame, text='Optimize', command=lambda: self.checkAndOptimize())
        trainModelButton.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        estTimeButton = tk.Button(trainFrame, text='Estimate running time',
                                  command=lambda: self.showTimeEstimateInformation())
        estTimeButton.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # TOOLTIPS ---------------
        layerTooltip = tt(layerHelp, 'Tooltip for Layers')
        nodeTooltip = tt(nodeHelp, 'Tooltip for Nodes')
        dropoutTooltip = tt(dropoutHelp, 'Tooltip for dropout percentage')
        learningTooltip = tt(learningHelp, 'Normally Values between 1e-3 and 1e-1 seem to be valuable')
        learningDecayTooltip = tt(learningDecayHelp, 'Learning Rate *= (1. / (1. + self.decay * self.iterations))')
        activationTooltip = tt(activationHelp, 'Tooltip for activation function')
        nbrOfModelsTooltip = tt(nbrOfModelsHelp, 'Number of models which are picked randomly from specified range.')

        # TOOLTIPS ---------------

        # Optimization process information
        optimizationInfoFrame = tk.Frame(self)
        optimizationInfoFrame.pack(fill=tk.X)
        self. optimizationInfoLabel = tk.Label(optimizationInfoFrame, text="", width=50)
        self. optimizationInfoLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

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
            return
        # Check the other parameters
        if not self.checkInputs():
            tk.messagebox.showwarning("Input Error", self.errorString)
            return
        # Check if data has been loaded
        if self.loadDataModel.data is None:
            self.loadDataModel.loadData()
        if self.loadDataModel.data is None:
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

            self.controlFrame.setProgressView(self.optimizeParamsModel, self.model, self.project)

    def checkInputs(self):
        self.errorString = ""
        minLayers = self.entryNbrMinLayers.get()
        maxLayers = self.entryNbrMaxLayers.get()
        if (minLayers == "") or (maxLayers == ""):
            self.errorString += "Insufficient entries in Layers\n"
            return False
        if int(minLayers) > int(maxLayers):
            self.errorString += "Min Layers must be smaller than Max Layers\n"
        if (int(minLayers) < 1) or (int(maxLayers) < 1):
            self.errorString += "Min Number of Layers are: 1\n"
        if (int(minLayers) > self.MAX_LAYERS) or (int(maxLayers) > self.MAX_LAYERS):
            self.errorString += "Max Number of Layers is: {}\n".format(self.MAX_LAYERS)

        minNodes = self.entryNbrMinNodes.get()
        maxNodes = self.entryNbrMaxNodes.get()
        if (minNodes == "") or (maxNodes == ""):
            self.errorString += "Insufficient entries in Nodes\n"
            return False
        if int(minNodes) > int(maxNodes):
            self.errorString += "Min Nodes must be smaller than Max Nodes\n"
        if (int(minNodes) < 1) or (int(maxNodes) < 1):
            self.errorString += "Min Number of Nodes are: 1\n"
        if (int(minNodes) > self.MAX_NODES) or (int(maxNodes) > self.MAX_NODES):
            self.errorString += "Max Number of nodes per layer is: {}\n".format(self.MAX_NODES)

        minDropout = self.entryNbrMinDropout.get()
        maxDropout = self.entryNbrMaxDropout.get()
        if (minDropout == "") or (maxDropout == ""):
            self.errorString += "Insufficient entries in Dropout\n"
            return False
        if int(minDropout) > int(maxDropout):
            self.errorString += "Min Dropout must be smaller than Max Dropout\n"
        if (int(minDropout) < 1) or (int(maxDropout) < 1):
            self.errorString += "Min Number of Dropout is: 1(%)\n"
        if (int(minDropout) > 99) or (int(maxDropout) > 99):
            self.errorString += "Max Number of Dropout is: 99(%)\n"

        minLearning = self.entryNbrMinLearning.get()
        maxLearning = self.entryNbrMaxLearning.get()
        if (minLearning == "") or (maxLearning == ""):
            self.errorString += "Insufficient entries in Learning rate\n"
            return False
        if int(minLearning) < int(maxLearning):
            self.errorString += "Number of min Learning has to be greater than max Learning (negative Number)\n"
        if (int(minLearning) > 7) or (int(minLearning) < 0) or (int(maxLearning) > 7) or (int(maxLearning) < 0):
            self.errorString += "Learning rate has to be between 7 and 0\n"

        minLearningDecay = self.entryNbrMinLearningDecay.get()
        maxLearningDecay = self.entryNbrMaxLearningDecay.get()
        if (minLearningDecay == "") or (maxLearningDecay == ""):
            self.errorString += "Insufficient entries in Learning rate\n"
        if int(minLearningDecay) < int(maxLearningDecay):
            self.errorString += "Number of min Learning has to be greater than max Learning (negative Number)\n"
        if (int(minLearningDecay) > 10) or (int(minLearningDecay) < 1) or (int(maxLearningDecay) > 10) or (int(maxLearningDecay) < 1):
            self.errorString += "Learning rate has to be between 10 and 1\n"

        print(self.errorString)
        if self.errorString == "":
            return True
        return False

    def checkActivation(self):
        # Check if an activation function is set
        if (self.sigmoidVar.get() == 0) & (self.linearVar.get() == 0) & (self.softmaxVar.get() == 0) & \
                (self.tanhVar.get() == 0) & (self.reluVar.get() == 0) & (self.eluVar.get() == 0):
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
        # Check if at least one activation function has been chosen
        if not self.checkActivation():
            tk.messagebox.showwarning("Activation Error", "Please select at least one activation function!")
            return
        # Check the other parameters
        if not self.checkInputs():
            tk.messagebox.showwarning("Input Error", self.errorString)
            return
        # Check if data is loaded:
        if self.loadDataModel.data is None:
            self.loadDataModel.loadData()
        if self.loadDataModel.data is None:
            tk.messagebox.showwarning("Data Error", "No data has been loaded to project. Load data before optimizing.")
        stringTime, timeInSeconds = self.estimateTime()
        message = "The optimization will take approximately " + stringTime + " [hh:mm:ss]."
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
        minNbrOfNodes = int(self.entryNbrMinNodes.get())
        maxNbrOfNodes = int(self.entryNbrMaxNodes.get())
        minNbrOfLayers = int(self.entryNbrMinLayers.get())
        maxNbrOfLayers = int(self.entryNbrMaxLayers.get())
        minDropout = int(self.entryNbrMinDropout.get())
        maxDropout = int(self.entryNbrMaxDropout.get())
        minLearning = 10 ** -int(self.entryNbrMinLearning.get())
        maxLearning = 10 ** -int(self.entryNbrMaxLearning.get())
        minLearningDecay = 10 ** -int(self.entryNbrMinLearningDecay.get())
        maxLearningDecay = 10 ** -int(self.entryNbrMaxLearningDecay.get())
        activationArray = self.getActivationCheckBtnValues()
        nbrOfCategories = self.loadDataModel.nbrOfCategories
        # explanation of next line: shape of 3rd dataset (=[2]) of loadDataModel (=rawData), [1]=colnumbers)
        nbrOfFeatures = np.shape(self.loadDataModel.data[2])[1] - nbrOfCategories
        print("Min Number of Nodes: " + str(minNbrOfNodes))
        print("Max Number of Nodes: " + str(maxNbrOfNodes))
        print("Min Number of Layers: " + str(minNbrOfLayers))
        print("Max Number of Layers: " + str(maxNbrOfLayers))
        print("Min Number of Dropout: " + str(minDropout))
        print("Max Number of Dropout: " + str(maxDropout))
        print("Min Number of Learning: " + str(minLearning))
        print("Max Number of Learning: " + str(maxLearning))
        print("Min Number of Learning Decay: " + str(minLearningDecay))
        print("Max Number of Learning Decay: " + str(maxLearningDecay))
        print("Activation Array: " + str(activationArray))
        # activationArray = np.array(['sigmoid', 'elu', 'softmax'])

        self.rangeForHyperParamsObj = RangeForHyperParamsObj()
        self.rangeForHyperParamsObj.nbrOfHiddenLayersDict = dict({'min': minNbrOfLayers, 'max': maxNbrOfLayers})
        self.rangeForHyperParamsObj.nbrOfHiddenUnitsDict = dict({'min': minNbrOfNodes, 'max': maxNbrOfNodes})
        self.rangeForHyperParamsObj.dropOutDict = dict({'min': minDropout, 'max': maxDropout})
        self.rangeForHyperParamsObj.learningRateDict = dict({'min': minLearning, 'max': maxLearning})
        self.rangeForHyperParamsObj.learningRateDecayDict = dict({'min': minLearningDecay, 'max': maxLearningDecay})
        self.rangeForHyperParamsObj.activationArray = activationArray
        self.rangeForHyperParamsObj.nbrOfCategories = nbrOfCategories
        self.rangeForHyperParamsObj.nbrOfFeatures = nbrOfFeatures

    def setProject(self, project):
        self.project = project
        self.loadDataModel = self.dataInteraction.getLoadDataModel(self.project.projectId)
        self.loadDataModel.dataIsForTraining = True

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

