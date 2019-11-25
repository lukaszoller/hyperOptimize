import tkinter as tk  # python 3
import numpy as np
from matplotlib.figure import Figure
from tkinter import font as tkfont  # python 3
import matplotlib.pyplot as plt
from src.hyperOptimizeApp.view.HomeView import HomeView
from src.hyperOptimizeApp.view.ProjectView import ProjectView
from src.hyperOptimizeApp.view.ModelView import ModelView
from src.hyperOptimizeApp.view.OptimizeModelView import TrainModelView
from src.hyperOptimizeApp.view.LoadDataView import LoadDataView
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from src.hyperOptimizeApp.logic.viewInteraction.ModelModel import ModelModel
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame


class ControlFrame(tk.Frame):
    projectView = None
    homeView = None
    modelView = None
    trainModelView = None
    loadDataView = None

    def __init__(self, mainView, main, width, homeView=HomeView, projectView=ProjectView, modelView=ModelView,
                 trainModelView=TrainModelView, loadDataView=LoadDataView):
        tk.Frame.__init__(self, main)
        self.projectView = projectView
        self.homeView = homeView
        self.modelView = modelView
        self.trainModelView = trainModelView
        self.loadDataView = loadDataView

        self.projectView.addControlFrame(self)
        self.homeView.addControlFrame(self)
        self.modelView.addControlFrame(self)
        self.trainModelView.addControlFrame(self)
        self.loadDataView.addControlFrame(self)

        self.changeStyle("black")
        self.place(x=0, y=450, height=50, width=width)

        # Fenster Zeichen
        tk.Button(self, text="Home", command=lambda: showFrame(self.homeView)).pack(side=tk.LEFT, padx=5)
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
        mFile.add_command(label="Home", command=lambda: showFrame(self.homeView))
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

    def setProjectFrame(self, newProject=bool, project=DatabaseProjectModel()):
        if not newProject:
            self.projectView.setTopText("New Project")
            newProjectModel = DatabaseProjectModel()
            self.projectView.setProject(newProjectModel)
        else:
            self.projectView.setTopText(project.getProjectName())
            self.projectView.setProject(project)
        showFrame(self.projectView)

    def setModelFrame(self, newModel=bool, model=DatabaseModelModel()):
        if not newModel:
            self.modelView.setTopText("New Model")
            newModel = DatabaseModelModel()
            self.modelView.setModel(newModel)
        else:
            self.modelView.setTopText(model.getModelName())
            self.modelView.setModel(model)
        showFrame(self.modelView)

    def setTrainModelFrame(self, model=DatabaseModelModel):
        self.trainModelView.setModel(model)
        showFrame(self.trainModelView)

    def setLoadDataFrame(self):
        showFrame(self.loadDataView)

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
        WM_HEIGHT = 500
        WM_WIDTH = 800

        # Hauptfenster
        self.main.title("Test")
        self.main.geometry("{:}x{:}".format(WM_WIDTH, WM_HEIGHT))
        # main.attributes("-fullscreen", True)
        self.main.resizable(0, 0)

        homeView = HomeView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        projectView = ProjectView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        modelView = ModelView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        trainModelView = TrainModelView(self.main, WM_WIDTH, WM_HEIGHT - 50)
        loadDataView = LoadDataView(self.main, WM_WIDTH, WM_HEIGHT - 50)

        ControlFrame(self, self.main, WM_WIDTH, homeView, projectView, modelView, trainModelView)

        self.main.mainloop()

    # Function for closing
    def close(self):
        self.main.destroy()


def showFrame(frame):
    frame.tkraise()
