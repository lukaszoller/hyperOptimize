import tkinter as tk
from src.hyperOptimizeApp.logic.viewInteraction.HomeModel import HomeModel


class HomeView(tk.Frame):
    homeModel = HomeModel()
    controlFrame = None
    projects = []

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="yellow")
        self.place(relx=0, rely=0, height=height, width=width)

        # Welcome text on Startup
        welcomeText = tk.Label(self, text='Welcome to the Neuronal Network optimizing tool! \n'
                                          'You can start with a new Project or load an existing one by clicking on'
                                          'it in the list below.').grid(row=1, column=3)

        # Generate a list of all Projects and show it.
        self.projectListbox = tk.Listbox(self)
        self.fillProjectList()

        # Generate the Buttons and show them.
        newProjectButton = tk.Button(self, text='New Project',
                                     command=lambda: self.controlFrame.setProjectFrame(True, None))
        newProjectButton.grid(row=3, column=2)
        loadProjectButton = tk.Button(self, text='Load Project',
                                      command=lambda: self.passProject())
        loadProjectButton.grid(row=3, column=3, padx=20, pady=20)

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def passProject(self):
        projectNumber = self.projectListbox.curselection()[0]
        project = self.projects.__getitem__(projectNumber)
        self.controlFrame.setProjectFrame(False, project)

    def fillProjectList(self):
        self.projects = []
        self.projectListbox.delete(0, tk.END)
        self.projects = self.homeModel.getProjectList()
        for project in self.projects:
            self.projectListbox.insert(tk.END, project)
        self.projectListbox.grid(row=2, column=3)
