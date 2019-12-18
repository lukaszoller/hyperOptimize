import tkinter as tk  # python 3
from src.hyperOptimizeApp.logic.LoadDataModel import LoadDataModel
from src.hyperOptimizeApp.view.HomeView import HomeView
from src.hyperOptimizeApp.view.ProjectView import ProjectView
from src.hyperOptimizeApp.view.ModelView import ModelView
from src.hyperOptimizeApp.view.OptimizeModelView import OptimizeModelView
from src.hyperOptimizeApp.view.LoadDataView import LoadDataView
from src.hyperOptimizeApp.persistence.dbInteraction.DatabaseProjectModel import DatabaseProjectModel


class ControlFrame(tk.Frame):
    projectView = None
    homeView = None
    modelView = None
    optimizeModelView = None
    loadDataView = None
    loadClassifyDataView = None
    project = None

    def __init__(self, mainView, main, height, width, homeView, projectView, modelView,
                 optimizeModelView, loadDataView, loadClassifyDataView):
        tk.Frame.__init__(self, main)
        self.projectView = projectView
        self.homeView = homeView
        self.modelView = modelView
        self.optimizeModelView = optimizeModelView
        self.loadDataView = loadDataView
        self.loadClassifyDataView = loadClassifyDataView

        self.projectView.addControlFrame(self)
        self.homeView.addControlFrame(self)
        self.modelView.addControlFrame(self)
        self.optimizeModelView.addControlFrame(self)
        self.loadDataView.addControlFrame(self)
        self.loadClassifyDataView.addControlFrame(self)

        self.changeStyle("black")
        self.place(x=0, y=height-50, height=50, width=width)

        # Fenster Zeichen
        tk.Button(self, text="Home", command=lambda: self.setHomeFrame()).pack(side=tk.LEFT, padx=5)
        tk.Button(self, text="New Project", command=lambda: self.setProjectFrame(True, None)).pack(
            side=tk.LEFT, padx=5)
        self.backButton = tk.Button(self, text="Back to Project", command=lambda: self.backToProject())
        tk.Button(self, text="Quit", command=mainView.close).pack(side=tk.RIGHT, padx=5)

        #####################################################################################
        # Menu List
        #####################################################################################
        # (first the Bar)
        mBar = tk.Menu(main)

        # Menu Object "File" and "Style"
        mFile = tk.Menu(mBar)
        mView = tk.Menu(mBar)

        # Menu Objects in "File"
        mFile["tearoff"] = 0
        mFile.add_command(label="Home", command=lambda: self.setHomeFrame())
        mFile.add_separator()
        mFile.add_command(label="New Project", command=lambda: self.setProjectFrame(False, None))
        mFile.add_separator()
        mFile.add_command(label="Quit", command=mainView.close)

        # Menu Objects in "View"
        mView["tearoff"] = 0
        mView.add_radiobutton(label="Dark", underline=0, command=lambda: self.changeStyle("black"))
        mView.add_radiobutton(label="Bright", underline=0, command=lambda: self.changeStyle("white"))

        mBar.add_cascade(label="File", menu=mFile)
        mBar.add_cascade(label="View", menu=mView)
        main["menu"] = mBar
        showFrame(homeView)

    # Function for changing style
    def changeStyle(self, color):
        self.config(background=color)

    def setHomeFrame(self):
        self.homeView.fillProjectList()
        showFrame(self.homeView)
        self.project = None
        self.unshowBackButton()

    def setProjectFrame(self, newProject, project):
        if newProject:
            self.projectView.setTopText("New Project")
            newProjectModel = DatabaseProjectModel()
            newProjectModel.projectName = "New Project"
            self.projectView.setProject(newProjectModel)
        else:
            self.projectView.setTopText(project.getProjectName())
            self.projectView.setProject(project)
        showFrame(self.projectView)
        self.unshowBackButton()

    def setProjectFrameWithClassificationData(self, project, loadDataModel):
        self.projectView.setTopText(project.getProjectName())
        self.projectView.setProject(project)
        self.projectView.setClassificationLoadDataModel(loadDataModel)
        showFrame(self.projectView)
        self.unshowBackButton()

    def setModelFrame(self, model, project):
        self.modelView.setModel(model)
        self.modelView.setProject(project)
        showFrame(self.modelView)
        self.showBackButton()

    def setModelFrameWithParameters(self, model, project):
        self.modelView.setModel(model)
        self.modelView.setProject(project)
        self.modelView.setParameters()
        showFrame(self.modelView)
        self.showBackButton()

    def setOptimizeModelFrame(self, model, project):
        self.optimizeModelView.setModel(model)
        self.optimizeModelView.setProject(project)
        showFrame(self.optimizeModelView)
        self.showBackButton()

    def setLoadDataFrame(self, project):
        self.loadDataView.setProject(project)
        showFrame(self.loadDataView)

    def setLoadClassificationDataFrame(self, project):
        self.loadClassifyDataView.setProject(project)
        showFrame(self.loadClassifyDataView)
        self.showBackButton()

    def setProject(self, project):
        self.project = project

    def backToProject(self):
        self.setProjectFrame(False, self.project)

    def showBackButton(self):
        self.backButton.pack(side=tk.LEFT)

    def unshowBackButton(self):
        self.backButton.pack_forget()

class MainView:
    main = tk.Tk()

    def __init__(self):
        # Konstanten
        WM_HEIGHT = 600
        WM_WIDTH = 1000

        # Hauptfenster
        self.main.title("Test")
        self.main.geometry("{:}x{:}".format(WM_WIDTH, WM_HEIGHT))
        # main.attributes("-fullscreen", True)
        self.main.resizable(0, 0)

        homeView = HomeView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        projectView = ProjectView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        modelView = ModelView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        optimizeModelView = OptimizeModelView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        loadDataView = LoadDataView(self.main, WM_WIDTH, WM_HEIGHT - 50, LoadDataModel(), forTraining=True)
        loadClassifyDataView = LoadDataView(self.main, WM_WIDTH, WM_HEIGHT - 50, LoadDataModel(), forTraining=False)

        ControlFrame(self, self.main, WM_HEIGHT, WM_WIDTH, homeView, projectView, modelView, optimizeModelView, loadDataView,
                     loadClassifyDataView)

        self.main.mainloop()

    # Function for closing
    def close(self):
        self.main.destroy()


def showFrame(frame):
    frame.tkraise()
