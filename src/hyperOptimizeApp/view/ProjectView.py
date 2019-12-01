import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfile

from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from src.hyperOptimizeApp.logic.dbInteraction.ProjectInteractionModel import ProjectInteractionModel
from src.hyperOptimizeApp.logic.dbInteraction.ModelInteractionModel import ModelInteractionModel


def openFile():
    saverLoader = SaverLoader()
    file = askopenfile(mode='r', filetypes=[('csv Files', '*.csv')])
    if file is not None:
        saverLoader.setFileName(file.name)
        print(saverLoader.getEstTimeData())


class ProjectView(tk.Frame):
    controlFrame = None
    project = DatabaseProjectModel()
    projectInteract = ProjectInteractionModel()
    modelInteract = ModelInteractionModel()
    modelList = []
    modelRow = 0

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)
        self.topText = tk.StringVar()
        self.topText.set("Project")

        rowCount = 0

        # ROW 1
        topLabel = tk.Label(self, textvariable=self.topText).grid(row=rowCount, column=3)
        rowCount += 1

        # ROW 2
        nameLabel = tk.Label(self, text="Project Name").grid(row=rowCount, column=2)
        self.nameEntry = tk.Entry(self)
        self.nameEntry.insert(tk.END, self.project.projectName)
        self.nameEntry.grid(row=rowCount, column=3)
        rowCount += 1

        # ROW 3
        fileLabel = tk.Label(self, text="Data CSV").grid(row=rowCount, column=2)
        loadFileButton = tk.Button(self, text='Open', command=lambda: openFile())
        loadFileButton.grid(row=rowCount, column=3, pady=10)

        loadDataButton = tk.Button(self, text="Load data", command=lambda: self.controlFrame.setLoadDataFrame()) \
            .grid(row=rowCount, column=4)

        rowCount += 1

        # ROW 4
        self.modelListbox = tk.Listbox(self)
        self.fillListBox(rowCount)
        self.modelRow = rowCount
        rowCount += 1

        # ROW 5
        loadModelButton = tk.Button(self, text="Load Model", command=lambda: self.passModel()) \
            .grid(row=rowCount, column=1)
        newModelButton = tk.Button(self, text="New Model",
                                   command=lambda: self.controlFrame.setModelFrame(False, None)) \
            .grid(row=rowCount, column=2)
        rowCount += 1

        # ROW 6
        saveButton = tk.Button(self, text="Save Project", command=lambda: self.saveProject()).grid(row=rowCount, padx=5)
        deleteButton = tk.Button(self, text="Delete Project",
                                 command=lambda: self.confirmationBox()).grid(row=rowCount, column=5, padx=5)

        self.config(bg="grey")
        self.place(relx=0, rely=0, height=height, width=width)

    def setProject(self, project=DatabaseProjectModel()):
        self.project = project
        print(self.project.projectId)
        if self.project.projectId != 0:
            self.modelList = self.modelInteract.getModelsByProjectId(self.project.projectId)
        self.fillListBox(self.modelRow)

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
            self.projectInteract.saveProject(self.project)
            print("Project created")
        self.setTopText(projectName)

    def confirmationBox(self):
        answer = tk.messagebox.askyesno("Confirm deletion", "Are you sure to delete this Project\n"
                                                            "AND all associated Models?")
        if answer == 1:
            if self.project is not None:
                self.projectInteract.deleteProjectById(self.project.projectId)
                self.modelInteract.deleteModelsByProjectId(self.projectId)
                print("Project deleted")
                self.controlFrame.setHomeFrame()
            else:
                print("no project selected")
        else:
            print("nothing done.")

    def passModel(self):
        modelNumber = self.modelListbox.curselection()[0]
        model = self.modelList.__getitem__(modelNumber)
        self.controlFrame.setModelFrame(True, model)

    def fillListBox(self, rowCount):
        self.modelListbox.delete(0, tk.END)
        for model in self.modelList:
            self.modelListbox.insert(tk.END, model)
        self.modelListbox.grid(row=rowCount, column=1)
