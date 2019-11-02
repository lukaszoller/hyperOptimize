import tkinter as tk  # python 3
from tkinter import font as tkfont  # python 3
from src.hyperOptimizeApp.view.HomeView import HomeView
from src.hyperOptimizeApp.view.ProjectView import ProjectView


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
        tk.Button(self, text="New Project", command=lambda: showFrame(self.projectView)).pack(side=tk.LEFT, padx=5)
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
        mFile.add_command(label="New Project", command=lambda: showFrame(self.projectView))
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

    def setProjectFrame(self):
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

        self.main.mainloop()

    # Function for closing
    def close(self):
        self.main.destroy()


def showFrame(frame):
    frame.tkraise()
