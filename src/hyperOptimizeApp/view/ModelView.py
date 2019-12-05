import tkinter as tk
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from src.hyperOptimizeApp.view import LayoutConstants
from src.hyperOptimizeApp.view import ValidationFunctions


class ModelView(tk.Frame):
    model = MachineLearningModel
    controlFrame = None
    project = DatabaseProjectModel()

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)
        self.topText = tk.StringVar()
        self.topText.set("Model")

        # Title of subwindow
        titleFrame = tk.Frame(self)
        titleFrame.pack(fill=tk.X)
        titleLabel = tk.Label(titleFrame, text="Modelname: " + str(self.topText), width=50, font=("Helvetica", 12))
        titleLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Number of Layers and Nodes
        nbrLayersNodesFrame = tk.Frame(self)
        nbrLayersNodesFrame.pack(fill=tk.X)
        nbrLayersLabel = tk.Label(nbrLayersNodesFrame, text="Input number of Layers:")
        nbrLayersLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        nbrLayersValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entryNbrLayers = tk.Entry(nbrLayersNodesFrame, width=10, validate="key",
                                       validatecommand=(nbrLayersValidation, '%S'))
        self.entryNbrLayers.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        nbrNodesLabel = tk.Label(nbrLayersNodesFrame, text="Input number of Nodes:")
        nbrNodesLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        nbrNodesValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entryNbrNodes = tk.Entry(nbrLayersNodesFrame, width=10, validate="key",
                                      validatecommand=(nbrNodesValidation, '%S'))
        self.entryNbrNodes.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)

        # Dropout
        dropoutFrame = tk.Frame(self)
        dropoutFrame.pack(fill=tk.X)
        dropoutLabel = tk.Label(dropoutFrame, text='Percentage of nodes weights set to 0:')
        dropoutLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.dropoutSlider = tk.Scale(dropoutFrame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01)
        self.dropoutSlider.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Frame with picking of different activation Functions
        self.activationCheckBtnDict = dict()
        activationFrame = tk.Frame(self)
        activationFrame.pack(fill=tk.X)
        ## Sigmoid
        sigmoidBoxName = "Sigmoid Function"
        activationLabel = tk.Label(activationFrame, text='Activation functions to choose:')
        activationLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.sigmoidVar = tk.IntVar(0)
        sigmoidBox = tk.Checkbutton(activationFrame, text=sigmoidBoxName, variable=self.sigmoidVar)
        sigmoidBox.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.activationCheckBtnDict['sigmoid'] = sigmoidBox
        ## Linear
        linearBoxName = "Linear Function"
        self.linearVar = tk.IntVar(0)
        linearBox = tk.Checkbutton(activationFrame, text=linearBoxName, variable=self.linearVar)
        linearBox.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.activationCheckBtnDict['linear'] = linearBox
        ## Tanh
        tanhBoxName = "Tanh Function"
        self.tanhVar = tk.IntVar(0)
        tanhBox = tk.Checkbutton(activationFrame, text=tanhBoxName, variable=self.tanhVar)
        tanhBox.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.activationCheckBtnDict['tanh'] = tanhBox
        ## Relu
        reluBoxName = "ReLu Function"
        self.reluVar = tk.IntVar(0)
        reluBox = tk.Checkbutton(activationFrame, text=reluBoxName, variable=self.reluVar)
        reluBox.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.activationCheckBtnDict['relu'] = reluBox

        # Optimize btn
        optimizeBtnFrame = tk.Frame(self)
        optimizeBtnFrame.pack(fill=tk.X)
        optimizeBtn = tk.Button(optimizeBtnFrame, text='Optimize Model',
                                         command=lambda: self.controlFrame.setOptimizeModelFrame(self.model, self.project))
        optimizeBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.optimizeInformation = tk.Label(optimizeBtnFrame, text="")
        self.optimizeInformation.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # # ROW 2
        # trainModelButton = tk.Button(self, text='Optimize Model',
        #                              command=lambda: self.controlFrame.setOptimizeModelFrame(self.model, self.project))\
        #     .grid(row=rowCount, column=3)
        # rowCount += 1

    def setProject(self, project=DatabaseProjectModel):
        self.project = project

    def setModel(self, model=MachineLearningModel):
        self.model = model

    def setTopText(self, text):
        self.topText.set(text)

    def addControlFrame(self, frame):
        self.controlFrame = frame
