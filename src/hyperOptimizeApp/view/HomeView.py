import tkinter as tk
from src.hyperOptimizeApp.logic.HomeModel import HomeModel


class HomeView(tk.Frame):
    homeModel = HomeModel()
    controlFrame = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="yellow")
        self.place(relx=0, rely=0, height=height, width=width)

        # Welcome text on Startup
        welcomeText = tk.Label(self, text='Welcome to the Neuronal Network optimizing tool! \n'
                                          'You can start with a new Project or load an existing one by clicking on'
                                          'it in the list below.').pack(side=tk.TOP)

        # Generate a list of all Projects and show it.
        self.projectList = self.homeModel.getProjectList()
        self.projectListbox = tk.Listbox(self)
        for project in self.projectList:
            self.projectListbox.insert(tk.END, project)
        self.projectListbox.pack(side=tk.TOP, pady=10)

        # Generate the Buttons and show them.
        loadFileButton = tk.Button(self, text='New Project',
                                   command=lambda: self.controlFrame.setProjectFrame(False, None))
        loadFileButton.pack(side=tk.BOTTOM, pady=2)
        loadFileButton = tk.Button(self, text='Load Project',
                                   command=lambda:
                                   self.passProject())
        loadFileButton.pack(side=tk.BOTTOM, pady=2)

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def passProject(self):
        projectNumber = self.projectListbox.curselection()[0]
        project = self.projectList.__getitem__(projectNumber)
        self.controlFrame.setProjectFrame(True, project)


