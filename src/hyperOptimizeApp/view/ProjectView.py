import tkinter as tk
import tkinter.messagebox
from tkinter import simpledialog

from src.hyperOptimizeApp.persistence.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from src.hyperOptimizeApp.persistence.dbInteraction.ProjectInteractionModel import ProjectInteractionModel
from src.hyperOptimizeApp.persistence.dbInteraction.ModelInteractionModel import ModelInteractionModel
from src.hyperOptimizeApp.view.tools import LayoutConstants
import re
import numpy as np


class ProjectView(tk.Frame):
    controlFrame = None
    project = DatabaseProjectModel()
    projectInteract = ProjectInteractionModel()
    modelInteract = ModelInteractionModel()
    modelList = []
    loadDataModelForClassification = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)
        self.topText = tk.StringVar()
        self.topText.set("Project")

        # ROW 1 - Top Label
        topTextFrame = tk.Frame(self)
        topTextFrame.pack(fill=tk.X)
        topLabel = tk.Label(topTextFrame, textvariable=self.topText)
        topLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # ROW 2 - Project Name
        projectNameFrame = tk.Frame(self)
        projectNameFrame.pack(fill=tk.X)
        nameLabel = tk.Label(projectNameFrame, text="Project Name:")
        nameLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.nameEntry = tk.Entry(projectNameFrame)
        self.fillNameLabel()

        # ROW 3 - File Handling for training and test data
        fileSelectionFrame = tk.Frame(self)
        fileSelectionFrame.pack(fill=tk.X)
        fileLabel = tk.Label(fileSelectionFrame, text="Data CSV")
        fileLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.fileSetLabel = tk.Label(fileSelectionFrame, text='Select Data:')
        self.fileSetLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.loadDataButton = tk.Button(fileSelectionFrame, text="Load data",
                                        command=lambda: self.saveProjectAndLoadData())
        self.loadDataButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # ROW 4 - List of Models
        modelListFrame = tk.Frame(self)
        modelListFrame.pack(fill=tk.X)
        self.modelListbox = tk.Listbox(modelListFrame)
        self.fillListBox()

        # ROW 5 - Model Buttons
        modelButtonFrame = tk.Frame(self)
        modelButtonFrame.pack(fill=tk.X)
        newModelButton = tk.Button(modelButtonFrame, text="New Model",
                                   command=lambda: self.saveAndAddNewModel())
        newModelButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        loadModelButton = tk.Button(modelButtonFrame, text="Load Model",
                                    command=lambda: self.saveAndPassModel())
        loadModelButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        deleteModelButton = tk.Button(modelButtonFrame, text="Delete Model",
                                      command=lambda: self.saveConfirmAndDeleteModel())
        deleteModelButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        self.config(bg="grey")
        self.place(relx=0, rely=0, height=height, width=width)

        # ROW 6 - File Handling for classifying data
        fileSelectionClassifyFrame = tk.Frame(self)
        fileSelectionClassifyFrame.pack(fill=tk.X)
        fileClassifyLabel = tk.Label(fileSelectionClassifyFrame, text="Data CSV")
        fileClassifyLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.fileClassifySetLabel = tk.Label(fileSelectionClassifyFrame, text='Select Data for classification:')
        self.fileClassifySetLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.loadClassifyDataButton = tk.Button(fileSelectionClassifyFrame, text="Load classification data",
                                        command=lambda: self.loadClassificationData())
        self.loadClassifyDataButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.classifyDataPathLabel = tk.Label(fileSelectionClassifyFrame, text="No data for classification selected")
        self.classifyDataPathLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)


        # ROW 7 - Classify data button
        classifyButtonFrame = tk.Frame(self)
        classifyButtonFrame.pack(fill=tk.X)
        classifyButton = tk.Button(classifyButtonFrame, text="Classify data",
                                   command=lambda: self.classifyData())
        classifyButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

    def classifyData(self):
        """Classifies a dataset. That means it adds some columns to the dataset with categories and writes it to the
        filesyste. Checks execuded first: model is selected, data is loaded."""


        # Get model
        if not self.modelListbox.curselection() is ():
            modelNumber = self.modelListbox.curselection()[0]
            model = self.modelList.__getitem__(modelNumber)
        else:
            tk.messagebox.showwarning("Error", "Select model before classifying data.")
            return

        # Check if data is loaded
        xData, yData, rawData = self.loadDataModelForClassification.data
        pathToFile = self.loadDataModelForClassification.pathToDataSet
        if self.loadDataModelForClassification == None:
            tk.messagebox.showwarning("Error", "No data is loaded")
            return


        # Check if data for classification has correct shape
        if not (np.shape(xData)[1] == model.getNbrOfFeatures()):
            tk.messagebox.showwarning("Error",
                                      "Data for classification has not same nbr of colums as features in training data.\n"
                                      "Expected: " + str(np.shape(xData)[0]) + "Actual shape of classification data: " +
                                      str(model.getNbrOfFeatures()))
            return

        # classify data
        classifiedData = model.predict(xData)
        # write data to filesystem
        try:
            pathToWrite = re.sub('.csv$', '_classified.csv', pathToFile)
            np.savetxt(pathToWrite, classifiedData)
        except:
            tk.messagebox.showwarning("Error", "Could not write data to file.")

    def setProject(self, project=DatabaseProjectModel()):
        self.project = project
        print(self.project.projectId)
        if self.project.projectId != 0:
            self.modelList = self.modelInteract.getModelsByProjectId(self.project.projectId)
            if self.project.dataIsSet:
                self.loadDataButton.pack_forget()
                self.fileSetLabel.config(text="Data is Set.")
            else:
                self.loadDataButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
                self.fileSetLabel.config(text="Select Data")
        else:
            self.loadDataButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
            self.fileSetLabel.config(text="Please add Project Name and Set your Data")
        self.fillListBox()
        self.fillNameLabel()

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def setTopText(self, text):
        self.topText.set(text)

    def saveProject(self):
        projectName = str(self.nameEntry.get())
        self.project.projectName = projectName
        if self.project.projectId != 0:
            self.projectInteract.saveProjectById(self.project)
            print("Project saved")
        else:
            self.project = self.projectInteract.saveProject(self.project)
            self.loadDataButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
            self.fileSetLabel.config(text="Select Data")
            print("Project created")
        self.controlFrame.setProject(self.project)
        self.setTopText(projectName)

    def saveConfirmAndDeleteModel(self):
        self.saveProject()
        self.confirmAndDeleteModel()

    def saveProjectAndLoadData(self):
        self.saveProject()
        self.controlFrame.setLoadDataFrame(self.project)

    def loadClassificationData(self):
        self.controlFrame.setLoadClassificationDataFrame(self.project)
        if not self.loadDataModelForClassification == None:
            self.classifyDataPathLabel.config(text="Classification data available.", bg="green")

    def setClassificationLoadDataModel(self, loadDataModel):
        self.loadDataModelForClassification =loadDataModel

    def saveAndAddNewModel(self):
        self.saveProject()
        self.addNewModel()

    def saveAndPassModel(self):
        self.saveProject()
        self.passModel()

    def confirmAndDeleteModel(self):
        if not self.modelListbox.curselection() is ():
            answer = tk.messagebox.askyesno("Confirm deletion", "Are you sure to delete this Model\n"
                                                            "AND all associated training progress?")
            if answer == 1:
                modelNumber = self.modelListbox.curselection()[0]
                model = self.modelList.__getitem__(modelNumber)
                self.modelInteract.deleteModelById(model.modelId)
                self.fillListBox()
                print("Model deleted")
            else:
                print("Nothing done.")
        else:
            print("No Model selected")


    def addNewModel(self):
        if not self.project.dataIsSet:
            tk.messagebox.showwarning("Activation Error", "Please select the data for your Project first.")
        else:
            modelName = tk.simpledialog.askstring("Input", "User friendly name of the Model:")
            if modelName == "":
                print("Model not created")
            else:
                try:
                    self.modelInteract.addModelByProjectId(modelName, self.project.projectId)
                    print("Model created")
                    self.controlFrame.setModelFrame(self.modelInteract.lastModel, self.project)
                except:
                    print("Model creation failed")

    def passModel(self):
        if not self.modelListbox.curselection() is ():
            modelNumber = self.modelListbox.curselection()[0]
            model = self.modelList.__getitem__(modelNumber)
            self.controlFrame.setModelFrame(model, self.project)
        else:
            print("No Model selected")

    def fillListBox(self):
        self.modelListbox.delete(0, tk.END)
        self.modelList = self.modelInteract.getModelsByProjectId(self.project.projectId)
        for model in self.modelList:
            self.modelListbox.insert(tk.END, model.modelName)
        self.modelListbox.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

    def fillNameLabel(self):
        self.nameEntry.delete(0, tk.END)
        self.nameEntry.insert(tk.END, self.project.projectName)
        self.nameEntry.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
