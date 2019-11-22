import tkinter as tk  # python 3
import numpy as np
from matplotlib.figure import Figure
from tkinter import font as tkfont  # python 3
import matplotlib.pyplot as plt
from src.hyperOptimizeApp.view.HomeView import HomeView
from src.hyperOptimizeApp.view.ProjectView import ProjectView
from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame




class ControlFrame(tk.Frame):
    projectView = None
    homeView = None

    def __init__(self, mainView, main, width, homeView, projectView):
        tk.Frame.__init__(self, main)
        self.projectView = projectView
        self.homeView = homeView

        self.projectView.addControlFrame(self)
        self.homeView.addControlFrame(self)

        self.changeStyle("black")
        self.place(x=0, y=450, height=50, width=width)

        # Fenster Zeichen
        tk.Button(self, text="Home", command=lambda: showFrame(self.homeView)).pack(side=tk.LEFT, padx=5)
        tk.Button(self, text="New Project", command=lambda: self.setProjectFrame(False, "New Project")).pack(
            side=tk.LEFT, padx=5)
        tk.Button(self, text="Quit", command=mainView.close).pack(side=tk.LEFT, padx=5)

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
        mFile.add_command(label="New Project", command=lambda: self.setProjectFrame(False, None))
        mFile.add_command(label="Load Project")
        mFile.add_command(label="Save")
        mFile.add_separator()
        mFile.add_command(label="Quit", command=mainView.close)

        # Menu Objects in "View"
        mView["tearoff"] = 0
        mView.add_radiobutton(label="Dark", underline=0, command=self.changeStyle("black"))
        mView.add_radiobutton(label="Bright", underline=0, command=self.changeStyle("white"))

        mBar.add_cascade(label="File", menu=mFile)
        mBar.add_cascade(label="View", menu=mView)
        main["menu"] = mBar
        showFrame(homeView)

    # Function for changing style
    def changeStyle(self, color):
        self.config(background=color)

    def setProjectFrame(self, newProject=bool, project=ProjectModel()):
        if not newProject:
            self.projectView.setTopText("New Project")
            newProjectModel = ProjectModel()
            self.projectView.setProject(newProjectModel)
        else:
            self.projectView.setTopText(project.getProjectName())
            self.projectView.setProject(project)
        showFrame(self.projectView)


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

        ControlFrame(self, self.main, WM_WIDTH, homeView, projectView)

        ########################################### Lukas Code #########################################

        plotButton = tk.Button(self.main, text="open new window with plot", command=self.showWindowWithPlot())
        plotButton.pack(side='left')

        newWindowButton = tk.Button(self.main, text="Open new window with text", command=self.showNewWindow())
        newWindowButton.pack(side='right')
        ########################################### Lukas Code #########################################

        self.main.mainloop()

    # Function for closing
    def close(self):
        self.main.destroy()

    def showWindowWithPlot(self):
        newWindow = tk.Toplevel(self.main)
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
        window = tk.Toplevel(self.main)
        message = "New window message."
        tk.Label(window, text=message).pack()

def showFrame(frame):
    frame.tkraise()
