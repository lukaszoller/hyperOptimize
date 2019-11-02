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
        projectList = self.homeModel.getProjectList()
        projectListbox = tk.Listbox(self)
        for item in projectList:
            projectListbox.insert(tk.END, item)
        projectListbox.pack(side=tk.TOP, pady=10)

        # Generate the Buttons and show them.
        loadFileButton = tk.Button(self, text='New Project', command=lambda: self.controlFrame.setProjectFrame())
        loadFileButton.pack(side=tk.BOTTOM, pady=2)
        loadFileButton = tk.Button(self, text='Load Project')
        loadFileButton.pack(side=tk.BOTTOM, pady=2)

    def addControlFrame(self, frame):
        self.controlFrame = frame
