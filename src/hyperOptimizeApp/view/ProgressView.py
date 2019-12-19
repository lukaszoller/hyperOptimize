import tkinter as tk
import logging
from tkinter.scrolledtext import ScrolledText
from src.hyperOptimizeApp.persistence.dbInteraction.ModelInteractionModel import ModelInteractionModel
from tkinter.messagebox import askyesno
from src.hyperOptimizeApp.view.tools.TextHandler import TextHandler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ProgressView(tk.Frame):
    modelInteraction = ModelInteractionModel()
    optimizeParamsModel = None
    controlFrame = None
    model = None
    project = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)

        topText = tk.Label(self, text='Progress of optimization:')
        topText.pack()

        self.scrolledText = ScrolledText(self, state='disabled')
        self.scrolledText.configure(font='TkFixedFont')
        self.scrolledText.pack()

    def setModel(self, model):
        self.model = model

    def setProject(self, project):
        self.project = project

    def setOptimizeModel(self, optimizeParamsModel):
        self.optimizeParamsModel = optimizeParamsModel

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def start(self):
        self.registerLogger()
        self.startOptimization()

    def startOptimization(self):
        answer = tk.messagebox.askyesno("Start Optimization?", "Start Optimization?")

        if answer == 1:
            self.optimizeParamsModel.evaluateModels()

        # ToDo: after best model is computed change back to model view and display modelparams in corresponding fields.
        bestModel = self.optimizeParamsModel.getBestModel()
        print("Best Model evaluated:", bestModel)

        # Update model with optimized params
        self.modelInteraction.updateModelParams(self.model, bestModel)
        # Indicate visually that the model has been trained (again).
        if "[Trained]" not in self.model.modelName:
            self.model.modelName = self.model.modelName + " [Trained]"
            self.modelInteraction.setModelByIdAsTrained(self.model, self.model.modelId)
        self.model = self.modelInteraction.getModelById(self.model.modelId)

        ## todo: delete after debugging
        self.optimizeParamsModel.visualizeHyperparamsPerformance()

        # Pop up asking for results to show
        self.askShowResults()

    def askShowResults(self):
        answer = tk.messagebox.askyesno("Show Results?", "Optimal Model found.\n"
                                                         "Do you want to see the result graph?")

        self.controlFrame.setModelFrameWithParameters(self.model, self.project)

        if answer == 1:
            self.showResultsPlot()

    def showResultsPlot(self):
        resultsWindow = tk.Toplevel(self)
        resultsWindow.title("Results of Optimization")

        # plot
        # figure = plt.Figure(figsize=(6, 5), dpi=100)
        figure = self.optimizeParamsModel.getResultsPlot()
        plot = FigureCanvasTkAgg(figure, resultsWindow)
        plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    # def setMaxNodeValue(self, number):
    #     self.maxNodeSliderValue.set(number)
    #     self.nodeSlider.configure(to=self.maxNodeSliderValue.get())

    def registerLogger(self):
        # Create textLogger
        text_handler = TextHandler(self.scrolledText)

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)
        self.optimizeParamsModel.registerLogger(logger)
        print("logger registered")
