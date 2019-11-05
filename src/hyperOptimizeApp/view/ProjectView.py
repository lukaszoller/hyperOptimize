import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfile

from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader
from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel


def openFile():
    saverLoader = SaverLoader()
    file = askopenfile(mode='r', filetypes=[('csv Files', '*.csv')])
    if file is not None:
        saverLoader.setFileName(file.name)
        print(saverLoader.getEstTimeData())


class ProjectView(tk.Frame):

    controlFrame = None
    project = ProjectModel()

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)
        self.topText = tk.StringVar()
        self.topText.set("Project")

        topLabel = tk.Label(self, textvariable=self.topText).pack(side=tk.TOP)

        self.projectFile = tk.StringVar().set(self.project.projectName)
        fileLabel = tk.Label(self, textvariable=self.projectFile)

        self.config(bg="grey")
        self.place(relx=0, rely=0, height=height, width=width)
        loadFileButton = tk.Button(self, text='Open', command=lambda: openFile())
        loadFileButton.pack(side=tk.TOP, pady=10)

        saveButton = tk.Button(self, text="Save Project").pack(side=tk.BOTTOM, padx=5)
        deleteButton = tk.Button(self, text="Delete Project",
                                 command=lambda: self.confirmationBox()).pack(side=tk.BOTTOM, padx=5)

    def setProject(self, project=ProjectModel):
        self.project = project

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def setTopText(self, text):
        self.topText.set(text)

    def confirmationBox(self):
        answer = tk.messagebox.askyesno("Confirm deletion", "Are you sure to delete this Project?")
        if answer == 1:
            print("Project Deleted")
