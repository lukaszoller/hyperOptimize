import tkinter as tk
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from src.hyperOptimizeApp.view.tools import LayoutConstants
from src.hyperOptimizeApp.view import ValidationFunctions
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import createHyperParamsListRandom
from src.hyperOptimizeApp.logic.dbInteraction.DataInteractionModel import DataInteractionModel


class ModelView(tk.Frame):
    model = None
    controlFrame = None
    project = None
    dataInteraction = DataInteractionModel()
    loadDataModel = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)
        self.topText = tk.StringVar()
        self.topText.set("Model Name: ")

        # Title of subwindow
        titleFrame = tk.Frame(self)
        titleFrame.pack(fill=tk.X)
        self.titleLabel = tk.Label(titleFrame, textvariable=self.topText, width=50, font=("Helvetica", 12))
        self.titleLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Optimize button row
        optimizeButtonFrame = tk.Frame(self)
        optimizeButtonFrame.pack(fill=tk.X)
        optimizeBtn = tk.Button(optimizeButtonFrame, text='Get model hyperparams by optimization',
                                command=lambda: self.controlFrame.setOptimizeModelFrame(self.model, self.project))
        optimizeBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.optimizeInformation = tk.Label(optimizeButtonFrame, text="")
        self.optimizeInformation.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        ### Enable / disable / train - button row
        disableEnableTrainFrame = tk.Frame(self)
        disableEnableTrainFrame.pack(fill=tk.X)
        # Enable manual hyperparameter setting
        enableManuallyBtn = tk.Button(disableEnableTrainFrame, text='Enable manual hyperparams setting',
                                      command=lambda: self.enableManualHyperParams())
        enableManuallyBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.enableManuallyInformation = tk.Label(disableEnableTrainFrame, text="")
        self.enableManuallyInformation.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Disable manual hyperparameter setting
        disableManuallyBtn = tk.Button(disableEnableTrainFrame, text='Disable manual hyperparams setting',
                                       command=lambda: self.disableManualHyperParams())
        disableManuallyBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.disableManuallyInformation = tk.Label(disableEnableTrainFrame, text="")
        self.disableManuallyInformation.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Train model with manual hyperparams
        trainBtn = tk.Button(disableEnableTrainFrame, text='Train model with manually set hyperparams',
                             command=lambda: self.trainModel())
        trainBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.trainInformation = tk.Label(disableEnableTrainFrame, text="")
        self.trainInformation.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        #############################################################
        # Hyperparam fields
        #############################################################
        # initialize dict with input / display fields to disable / enable all of them
        self.inputFieldList = list()

        # Number of Layers and Nodes
        # Layers
        nbrLayersNodesFrame = tk.Frame(self)
        nbrLayersNodesFrame.pack(fill=tk.X)
        nbrLayersLabel = tk.Label(nbrLayersNodesFrame, text="Input number of Layers:")
        nbrLayersLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        nbrLayersValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entryNbrLayers = tk.Entry(nbrLayersNodesFrame, width=10, validate="key",
                                       validatecommand=(nbrLayersValidation, '%S'))
        self.entryNbrLayers.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.inputFieldList.append(self.entryNbrLayers)
        # Nodes
        nbrNodesLabel = tk.Label(nbrLayersNodesFrame, text="Input number of Nodes:")
        nbrNodesLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        nbrNodesValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entryNbrNodes = tk.Entry(nbrLayersNodesFrame, width=10, validate="key",
                                      validatecommand=(nbrNodesValidation, '%S'))
        self.entryNbrNodes.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.inputFieldList.append(self.entryNbrNodes)

        # Dropout
        dropoutFrame = tk.Frame(self)
        dropoutFrame.pack(fill=tk.X)
        dropoutLabel = tk.Label(dropoutFrame, text='Percentage of nodes weights set to 0:')
        dropoutLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.dropoutSlider = tk.Scale(dropoutFrame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        self.dropoutSlider.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.dropoutSlider)

        # Frame with picking of different activation Functions
        activationFrame = tk.Frame(self)
        activationFrame.pack(fill=tk.X)
        activationLabel = tk.Label(activationFrame, text='Activation functions to choose:')
        activationLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.activationVar = tk.IntVar()

        ## Sigmoid
        sigmoidRadioName = "Sigmoid Function"
        # self.sigmoidVar = tk.IntVar(0)
        sigmoidRadio = tk.Radiobutton(activationFrame, text=sigmoidRadioName, variable=self.activationVar,
                                      value="sigmoid")
        sigmoidRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(sigmoidRadio)

        ## Linear
        linearRadioName = "Linear Function"
        # self.linearVar = tk.IntVar(0)
        linearRadio = tk.Radiobutton(activationFrame, text=linearRadioName, variable=self.activationVar,
                                      value="linear")
        linearRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(linearRadio)

        ## Tanh
        tanhRadioName = "Tanh Function"
        # self.tanhVar = tk.IntVar(0)
        tanhRadio = tk.Radiobutton(activationFrame, text=tanhRadioName, variable=self.activationVar,
                                      value="tanh")
        tanhRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(tanhRadio)

        ## Relu
        reluRadioName = "ReLu Function"
        # self.reluVar = tk.IntVar(0)
        reluRadio = tk.Radiobutton(activationFrame, text=reluRadioName, variable=self.activationVar,
                                      value="relu")
        reluRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(reluRadio)

        # Initially disable input fields
        self.disableManualHyperParams()

    def setProject(self, project):
        self.project = project
        self.loadDataModel = self.dataInteraction.getLoadDataModel(self.project.projectId)
        self.loadDataModel.dataIsForTraining = True
        self.loadDataModel.loadData()

    def setModel(self, model):
        self.model = model
        self.setTopText()

    def setTopText(self):
        self.topText.set("Model Name: " + self.model.modelName)
        self.titleLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def enableManualHyperParams(self):
        for element in self.inputFieldList:
            element.config(state = "normal")

    def disableManualHyperParams(self):
        for element in self.inputFieldList:
            element.config(state="disabled")

    def trainModel(self):
        # get parameters
        rangeForHyperparamsObj = RangeForHyperParamsObj()
        minNbrOfNodes = self.entryNbrNodes.get()
        maxNbrOfNodes = minNbrOfNodes
        minNbrOfLayers = self.entryNbrLayers.get()
        maxNbrOfLayers = minNbrOfLayers
        minDropout = self.dropoutSlider.get()
        maxDropout = minDropout
        activationArray = self.activationVar.get()

        rangeForHyperParamsObj = RangeForHyperParamsObj()
        rangeForHyperParamsObj.nbrOfHiddenLayersDict = dict({'min': minNbrOfLayers, 'max': maxNbrOfLayers})
        rangeForHyperParamsObj.nbrOfHiddenUnitsDict = dict({'min': minNbrOfNodes, 'max': maxNbrOfNodes})
        rangeForHyperParamsObj.dropOutDict = dict({'min': minDropout, 'max': maxDropout})
        rangeForHyperParamsObj.activationArray = activationArray

        # Create hyperParamsObj
        hyperParamsObj = createHyperParamsListRandom(rangeForHyperParamsObj)

        # create and train model
        self.model.hyperParamsObj = hyperParamsObj
        self.model.train(self.getTrainData())

    def getTrainData(self):
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

