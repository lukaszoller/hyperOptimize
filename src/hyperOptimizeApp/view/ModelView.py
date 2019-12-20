import tkinter as tk
from tkinter.messagebox import showwarning
import numpy as np
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import RangeForHyperParamsObj
from src.hyperOptimizeApp.view.tools import LayoutConstants
from src.hyperOptimizeApp.view.tools import ValidationFunctions
from src.hyperOptimizeApp.logic.RangeForHyperParamsObj import createHyperParamsListRandom
from src.hyperOptimizeApp.persistence.dbInteraction.DataInteractionModel import DataInteractionModel
from src.hyperOptimizeApp.persistence.dbInteraction.ModelInteractionModel import ModelInteractionModel


class ModelView(tk.Frame):
    model = None
    controlFrame = None
    project = None
    dataInteraction = DataInteractionModel()
    modelInteraction = ModelInteractionModel()
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
        self.radioList = list()

        # Number of Layers and Nodes
        # Layers
        nbrLayersNodesFrame = tk.Frame(self)
        nbrLayersNodesFrame.pack(fill=tk.X)
        nbrLayersLabel = tk.Label(nbrLayersNodesFrame, text="Input number of Layers:")
        nbrLayersLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.nbrLayersValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entryNbrLayers = tk.Entry(nbrLayersNodesFrame, width=10, validate="key",
                                       validatecommand=(self.nbrLayersValidation, '%S'))
        self.entryNbrLayers.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.inputFieldList.append(self.entryNbrLayers)
        # Nodes
        nbrNodesLabel = tk.Label(nbrLayersNodesFrame, text="Input number of Nodes:")
        nbrNodesLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.nbrNodesValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entryNbrNodes = tk.Entry(nbrLayersNodesFrame, width=10, validate="key",
                                      validatecommand=(self.nbrNodesValidation, '%S'))
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

        # Learning Rate
        learningFrame = tk.Frame(self)
        learningFrame.pack(fill=tk.X)
        learningLabel = tk.Label(learningFrame, text='Negative Log of learning rate (From 7 to 1):')
        learningLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.learningSlider = tk.Scale(learningFrame, from_=7, to=1, orient=tk.HORIZONTAL, resolution=0.1)
        self.learningSlider.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.learningSlider)

        learningTrainingLabel = tk.Label(learningFrame, text="Value from optimization:")
        learningTrainingLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.learningVariable = tk.StringVar()
        self.learningLabel = tk.Label(learningFrame, textvariable=self.learningVariable, width=50, font=("Helvetica", 12))

        # Learning Rate Decay
        learningDecayFrame = tk.Frame(self)
        learningDecayFrame.pack(fill=tk.X)
        learningDecayLabel = tk.Label(learningDecayFrame, text='Negative Log of learning rate decay (From 10 to 1):')
        learningDecayLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.learningDecaySlider = tk.Scale(learningDecayFrame, from_=10, to=1, orient=tk.HORIZONTAL, resolution=0.1)
        self.learningDecaySlider.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.learningDecaySlider)

        learningDecayTrainingLabel = tk.Label(learningDecayFrame, text="Value from optimization:")
        learningDecayTrainingLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.learningDecayVariable = tk.StringVar()
        self.learningDecayLabel = tk.Label(learningDecayFrame, textvariable=self.learningDecayVariable, width=50, font=("Helvetica", 12))


        # Frame with picking of different activation Functions
        activationFrame = tk.Frame(self)
        activationFrame.pack(fill=tk.X)
        activationLabel = tk.Label(activationFrame, text='Activation functions to choose:')
        activationLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.activationVar = tk.StringVar("")

        ## Sigmoid
        sigmoidRadioName = "Sigmoid"
        self.sigmoidRadio = tk.Radiobutton(activationFrame, text=sigmoidRadioName, variable=self.activationVar,
                                      value="sigmoid")
        self.sigmoidRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.sigmoidRadio)
        self.radioList.append(self.sigmoidRadio)

        ## Linear
        linearRadioName = "Linear"
        self.linearRadio = tk.Radiobutton(activationFrame, text=linearRadioName, variable=self.activationVar,
                                      value="linear")
        self.linearRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.linearRadio)
        self.radioList.append(self.linearRadio)

        ## Tanh
        tanhRadioName = "Tanh"
        self.tanhRadio = tk.Radiobutton(activationFrame, text=tanhRadioName, variable=self.activationVar,
                                      value="tanh")
        self.tanhRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.tanhRadio)
        self.radioList.append(self.tanhRadio)

        ## elu
        eluRadioName = "eLu"
        self.eluRadio = tk.Radiobutton(activationFrame, text=eluRadioName, variable=self.activationVar,
                                       value="elu")
        self.eluRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.eluRadio)
        self.radioList.append(self.eluRadio)

        ## SoftMax
        softmaxRadioName = "SoftMax"
        self.softmaxRadio = tk.Radiobutton(activationFrame, text=softmaxRadioName, variable=self.activationVar,
                                    value="softmax")
        self.softmaxRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.softmaxRadio)
        self.radioList.append(self.softmaxRadio)

        ## Relu
        reluRadioName = "ReLu"
        self.reluRadio = tk.Radiobutton(activationFrame, text=reluRadioName, variable=self.activationVar,
                                      value="relu")
        self.reluRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.reluRadio)
        self.radioList.append(self.reluRadio)

        # Frame with picking of different model Optimizers
        optimizerFrame = tk.Frame(self)
        optimizerFrame.pack(fill=tk.X)
        optimizerLabel = tk.Label(optimizerFrame, text='Model opzimizers to choose:')
        optimizerLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.optimizerVar = tk.StringVar("")

        ## SGD
        SGDRadioName = "SGD"
        self.SGDRadio = tk.Radiobutton(optimizerFrame, text=SGDRadioName, variable=self.optimizerVar,
                                      value="SGD")
        self.SGDRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.SGDRadio)
        self.radioList.append(self.SGDRadio)

        # RMSprop
        RMSPropRadioName = "RMSprop"
        self.RMSPropRadio = tk.Radiobutton(optimizerFrame, text=RMSPropRadioName, variable=self.optimizerVar,
                                      value="RMSProp")
        self.RMSPropRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.RMSPropRadio)
        self.radioList.append(self.RMSPropRadio)

        # Adagrad
        adagradRadioName = "Adagrad"
        self.adagradRadio = tk.Radiobutton(optimizerFrame, text=adagradRadioName, variable=self.optimizerVar,
                                      value="Adagrad")
        self.adagradRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.adagradRadio)
        self.radioList.append(self.adagradRadio)

        # Adam
        adamRadioName = "Adam"
        self.adamRadio = tk.Radiobutton(optimizerFrame, text=adamRadioName, variable=self.optimizerVar,
                                      value="Adam")
        self.adamRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.adamRadio)
        self.radioList.append(self.adamRadio)

        # Nadam
        nadamRadioName = "Nadam"
        self.nadamRadio = tk.Radiobutton(optimizerFrame, text=nadamRadioName, variable=self.optimizerVar,
                                      value="Nadam")
        self.nadamRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.nadamRadio)
        self.radioList.append(self.nadamRadio)

        # Adaldelta
        adaldeltaRadioName = "Adaldelta"
        self.adaldeltaRadio = tk.Radiobutton(optimizerFrame, text=adaldeltaRadioName, variable=self.optimizerVar,
                                      value="Adaldelta")
        self.adaldeltaRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.adaldeltaRadio)
        self.radioList.append(self.adaldeltaRadio)

        # Frame with picking of different model Optimizers
        lossFunctionFrame = tk.Frame(self)
        lossFunctionFrame.pack(fill=tk.X)
        lossFunctionLabel = tk.Label(lossFunctionFrame, text='Loss functions to choose:')
        lossFunctionLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.lossVar = tk.StringVar("")

        # Mean Squared error
        mseRadioName = "Mean Squared Error"
        self.mseRadio = tk.Radiobutton(lossFunctionFrame, text=mseRadioName, variable=self.lossVar,
                                      value="mean_squared_error")
        self.mseRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.mseRadio)
        self.radioList.append(self.mseRadio)

        # Binary Crossentropy
        bcRadioName = "Binary Crossentropy"
        self.bcRadio = tk.Radiobutton(lossFunctionFrame, text=bcRadioName, variable=self.lossVar,
                                      value="binary_crossentropy")
        self.bcRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.bcRadio)
        self.radioList.append(self.bcRadio)

        # Mean Squared Log error
        msleRadioName = "Mean Squared Log error"
        self.msleRadio = tk.Radiobutton(lossFunctionFrame, text=msleRadioName, variable=self.lossVar,
                                      value="mean_squared_logarithmic_error")
        self.msleRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.msleRadio)
        self.radioList.append(self.msleRadio)

        # Hinge
        hingeRadioName = "Hinge"
        self.hingeRadio = tk.Radiobutton(lossFunctionFrame, text=hingeRadioName, variable=self.lossVar,
                                      value="hinge")
        self.hingeRadio.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.inputFieldList.append(self.hingeRadio)
        self.radioList.append(self.hingeRadio)

        self.deselectRadios()

        # Initially disable input fields
        self.disableManualHyperParams()

    def setProject(self, project):
        self.project = project
        self.loadDataModel = self.dataInteraction.getLoadDataModel(self.project.projectId)
        self.loadDataModel.dataIsForTraining = True

    def setModel(self, model):
        self.model = model
        self.setTopText()
        if "[Trained]" in self.model.modelName:
            self.setParameters()

    def setParameters(self):
        self.enableManualHyperParams()

        self.entryNbrLayers.configure(validatecommand=())
        self.entryNbrLayers.delete(0, tk.END)
        self.entryNbrLayers.insert(tk.END, len(self.model.hyperParamsObj.nbrOfNodesArray))
        print(len(self.model.hyperParamsObj.nbrOfNodesArray))
        self.entryNbrLayers.configure(validatecommand=(self.nbrLayersValidation, '%S'))
        self.entryNbrLayers.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.entryNbrNodes.configure(validatecommand=())
        self.entryNbrNodes.delete(0, tk.END)
        self.entryNbrNodes.insert(tk.END, self.model.hyperParamsObj.nbrOfNodesArray[1])
        print(self.model.hyperParamsObj.nbrOfNodesArray[1])
        self.entryNbrNodes.configure(validatecommand=(self.nbrNodesValidation, '%S'))
        self.entryNbrNodes.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        self.dropoutSlider.set(self.model.hyperParamsObj.dropOutRate)
        self.dropoutSlider.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        activationFunction = self.model.hyperParamsObj.activationFunction
        self.sigmoidRadio.deselect()
        self.tanhRadio.deselect()
        self.linearRadio.deselect()
        self.reluRadio.deselect()
        self.eluRadio.deselect()
        self.softmaxRadio.deselect()
        if activationFunction == 'sigmoid':
            self.sigmoidRadio.select()
        elif activationFunction == 'tanh':
            self.tanhRadio.select()
        elif activationFunction == 'linear':
            self.linearRadio.select()
        elif activationFunction == 'relu':
            self.reluRadio.select()
        elif activationFunction == 'elu':
            self.eluRadio.select()
        elif activationFunction == 'softmax':
            self.softmaxRadio.select()

        lossFunction = self.model.hyperParamsObj.lossFunction
        self.mseRadio.deselect()
        self.bcRadio.deselect()
        self.msleRadio.deselect()
        self.hingeRadio.deselect()
        if lossFunction == 'mean_squared_error':
            self.mseRadio.select()
        elif lossFunction == 'binary_crossentropy':
            self.bcRadio.select()
        elif lossFunction == 'mean_squared_logarithmic_error':
            self.msleRadio.select()
        elif lossFunction == 'hinge':
            self.hingeRadio.select()

        modelOptimizer = self.model.hyperParamsObj.modelOptimizer
        self.SGDRadio.deselect()
        self.RMSPropRadio.deselect()
        self.adagradRadio.deselect()
        self.adamRadio.deselect()
        self.nadamRadio.deselect()
        self.adaldeltaRadio.deselect()
        if modelOptimizer == 'SGD':
            self.SGDRadio.select()
        elif modelOptimizer == 'RMSprop':
            self.RMSPropRadio.select()
        elif modelOptimizer == 'Adagrad':
            self.adagradRadio.select()
        elif modelOptimizer == 'Adam':
            self.adamRadio.select()
        elif modelOptimizer == 'Nadam':
            self.nadamRadio.select()
        elif modelOptimizer == 'Adadelta':
            self.adaldeltaRadio.select()

        self.learningVariable.set(str(self.model.hyperParamsObj.learningRate))
        self.learningLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        self.learningDecayVariable.set(str(self.model.hyperParamsObj.learningRate))
        self.learningDecayLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        self.disableManualHyperParams()

    def setTopText(self):
        self.topText.set("Model Name: " + self.model.modelName)
        self.titleLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def enableManualHyperParams(self):
        for element in self.inputFieldList:
            element.config(state="normal")

    def disableManualHyperParams(self):
        for element in self.inputFieldList:
            element.config(state="disabled")

    def deselectRadios(self):
        self.lossVar.set(None)
        self.optimizerVar.set(None)
        self.activationVar.set(None)

    def trainModel(self):

        self.model.resetModel()
        self.loadDataModel.loadData()
        # get parameters
        nbrOfNodes = self.entryNbrNodes.get()
        nbrOfLayers = self.entryNbrLayers.get()
        dropout = self.dropoutSlider.get()
        activationFunction = self.activationVar.get()
        modelOptimizer = self.optimizerVar.get()
        lossFunction = self.lossVar.get()
        learning = 10 ** -int(self.learningSlider.get())
        learningDecay = 10 ** -int(self.learningDecaySlider.get())

        print(nbrOfNodes)
        print(nbrOfLayers)

        if (nbrOfNodes == "") or (nbrOfLayers == "") or (lossFunction == "None") or (modelOptimizer == "None") or (activationFunction == "None"):
            tk.messagebox.showwarning("Input error", "Please fill all input fields!")
            return

        rangeForHyperParamsObj = RangeForHyperParamsObj()
        rangeForHyperParamsObj.nbrOfHiddenLayersDict = dict({'min': nbrOfLayers, 'max': nbrOfLayers})
        rangeForHyperParamsObj.nbrOfHiddenUnitsDict = dict({'min': nbrOfNodes, 'max': nbrOfNodes})
        rangeForHyperParamsObj.dropOutDict = dict({'min': dropout, 'max': dropout})
        rangeForHyperParamsObj.learningRateDict = dict({'min': learning, 'max': learning})
        rangeForHyperParamsObj.learningRateDecayDict = dict({'min': learningDecay, 'max': learningDecay})
        rangeForHyperParamsObj.activationArray = np.array([activationFunction])
        rangeForHyperParamsObj.lossFunctionArray = np.array([lossFunction])
        rangeForHyperParamsObj.modelOptimizerArray = np.array([modelOptimizer])
        rangeForHyperParamsObj.nbrOfCategories = self.loadDataModel.nbrOfCategories

        x, y, rawData = self.loadDataModel.data
        rangeForHyperParamsObj.nbrOfFeatures = np.shape(rawData)[1] - rangeForHyperParamsObj.nbrOfCategories

        # Create hyperParamsObj
        hyperParamsObj = createHyperParamsListRandom(rangeForHyperParamsObj, 1)

        # create and train model
        self.model.hyperParamsObj = hyperParamsObj
        self.model.createNetwork()
        x_train, y_train, x_test, y_test = self.getTrainData()
        self.model.trainNetwork(x_train, y_train)

        # save model to db
        self.modelInteraction.updateModelParams(self.model, self.model)
        # Indicate visually that the model has been trained (again).
        if "[Trained]" not in self.model.modelName:
            self.model.modelName = self.model.modelName + " [Trained]"
            self.modelInteraction.setModelByIdAsTrained(self.model, self.model.modelId)
        self.model = self.modelInteraction.getModelById(self.model.modelId)

        self.controlFrame.setModelFrame(self.model, self.project)

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


