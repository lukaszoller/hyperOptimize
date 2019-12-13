import tkinter as tk  # python 3
import numpy as np
from matplotlib.figure import Figure
from tkinter import font as tkfont  # python 3
import matplotlib.pyplot as plt
from src.hyperOptimizeApp.logic.LoadDataModel import LoadDataModel
from src.hyperOptimizeApp.view.HomeView import HomeView
from src.hyperOptimizeApp.view.ProjectView import ProjectView
from src.hyperOptimizeApp.view.ModelView import ModelView
from src.hyperOptimizeApp.view.OptimizeModelView import OptimizeModelView
from src.hyperOptimizeApp.view.LoadDataView import LoadDataView
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame


class ControlFrame(tk.Frame):
    projectView = None
    homeView = None
    modelView = None
    optimizeModelView = None
    loadDataView = None
    loadClassifyDataView = None

    def __init__(self, mainView, main, width, homeView, projectView, modelView,
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
        self.place(x=0, y=750, height=50, width=width)

        # Fenster Zeichen
        tk.Button(self, text="Home", command=lambda: self.setHomeFrame()).pack(side=tk.LEFT, padx=5)
        tk.Button(self, text="New Project", command=lambda: self.setProjectFrame(False, "New Project")).pack(
            side=tk.LEFT, padx=5)
        tk.Button(self, text="Quit", command=mainView.close).pack(side=tk.LEFT, padx=5)

        ########################################### Lukas Code #########################################

        plotButton = tk.Button(self, text="open new window with plot", command=lambda: self.showWindowWithPlot())
        plotButton.pack(side=tk.LEFT, padx=5)

        newWindowButton = tk.Button(self, text="Open new window with text", command=lambda: self.showNewWindow())
        newWindowButton.pack(side=tk.LEFT, padx=5)
        ########################################### Lukas Code #########################################

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
        mFile.add_command(label="Load Project")
        mFile.add_command(label="Save")
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

    def setProjectFrameWithClassificationData(self, project, loadDataModel):
        self.projectView.setTopText(project.getProjectName())
        self.projectView.setProject(project)
        self.projectView.setClassificationLoadDataModel(loadDataModel)
        showFrame(self.projectView)

    def setModelFrame(self, model, project):
        self.modelView.setModel(model)
        self.modelView.setProject(project)
        showFrame(self.modelView)

    def setModelFrameWithParameters(self, model, project):
        self.modelView.setModel(model)
        self.modelView.setProject(project)
        self.modelView.setParameters()
        showFrame(self.modelView)

    def setOptimizeModelFrame(self, model, project):
        self.optimizeModelView.setModel(model)
        self.optimizeModelView.setProject(project)
        showFrame(self.optimizeModelView)

    def setLoadDataFrame(self, project):
        self.loadDataView.setProject(project)
        showFrame(self.loadDataView)

    def setLoadClassificationDataFrame(self, project):
        self.loadClassifyDataView.setProject(project)
        showFrame(self.loadClassifyDataView)

    # ########################################## Lukas Code #########################################

    def showWindowWithPlot(self):
        newWindow = tk.Toplevel(self)
        # get data
        Data1 = {'Country': ['US', 'CA', 'GER', 'UK', 'FR'],
                 'GDP_Per_Capita': [45000, 42000, 52000, 49000, 47000]
                 }

        df1 = DataFrame(Data1, columns=['Country', 'GDP_Per_Capita'])
        df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
        print(df1)

        # plot
        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, newWindow)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')

        newWindow.mainloop()

    def showNewWindow(self):
        window = tk.Toplevel(self)
        message = "New window message."
        tk.Label(window, text=message).pack()

    # ########################################## Lukas Code #########################################


class MainView:
    main = tk.Tk()

    def __init__(self):
        # Konstanten
        WM_HEIGHT = 800
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

        ControlFrame(self, self.main, WM_WIDTH, homeView, projectView, modelView, optimizeModelView, loadDataView,
                     loadClassifyDataView)

        self.main.mainloop()

    # Function for closing
    def close(self):
        self.main.destroy()


def showFrame(frame):
    frame.tkraise()
