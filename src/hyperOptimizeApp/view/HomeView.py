import tkinter as tk
import tkinter.messagebox

from src.hyperOptimizeApp.logic.viewInteraction.HomeModel import HomeModel
from src.hyperOptimizeApp.view.tools import LayoutConstants
from src.hyperOptimizeApp.logic.dbInteraction.ProjectInteractionModel import ProjectInteractionModel


class HomeView(tk.Frame):
    projectInteract = ProjectInteractionModel()
    homeModel = HomeModel()
    controlFrame = None
    projects = []

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="grey")
        self.place(relx=0, rely=0, height=height, width=width)


        # Title
        titleFrame = tk.Frame(self)
        titleFrame.pack(fill=tk.X)
        titleLabel = tk.Label(titleFrame, text="HyperOptimize", width=50, font=("Helvetica", 12))
        titleLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)


        # # Welcome text on Startup
        # welcomeText = tk.Label(self, text='Welcome to the Neuronal Network optimizing tool! \n'
        #                                   'You can start with a new Project or load an existing one by clicking on'
        #                                   'it in the list below.').grid(row=1, column=3)

        # Generate a list of all Projects and show it.
        projectFrame = tk.Frame(self)
        projectFrame.pack(fill=tk.X)
        self.projectListbox = tk.Listbox(projectFrame)
        self.fillProjectList()

        # Generate the Buttons and show them.
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(fill=tk.X)
        newProjectButton = tk.Button(buttonFrame, text='New Project',
                                     command=lambda: self.controlFrame.setProjectFrame(True, None))
        newProjectButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        loadProjectButton = tk.Button(buttonFrame, text='Load Project',
                                      command=lambda: self.passProject())
        loadProjectButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        deleteProjectButton = tk.Button(buttonFrame, text='Delete Project',
                                        command=lambda: self.confirmAndDeleteProject())
        deleteProjectButton.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

    def confirmAndDeleteProject(self):
        if not self.projectListbox.curselection() is ():
            answer = tk.messagebox.askyesno("Confirm deletion", "Are you sure to delete this Project\n"
                                                            "AND all associated Models?")
            if answer == 1:

                projectNumber = self.projectListbox.curselection()[0]
                project = self.projects.__getitem__(projectNumber)
                self.projectInteract.deleteProjectById(project.projectId)
                self.projectInteract.deleteModelsByProjectId(project.projectId)
                print("Project deleted")
                self.fillProjectList()
            else:
                print("Nothing done.")
        else:
            print("No Project selected")

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def passProject(self):
        if not self.projectListbox.curselection() is ():
            projectNumber = self.projectListbox.curselection()[0]
            project = self.projects.__getitem__(projectNumber)
            self.controlFrame.setProjectFrame(False, project)
        else:
            print("No Project selected")

    def fillProjectList(self):
        self.projects = []
        self.projectListbox.delete(0, tk.END)
        self.projects = self.homeModel.getProjectList()
        for project in self.projects:
            self.projectListbox.insert(tk.END, project)
        self.projectListbox.grid(row=1, column=1)
