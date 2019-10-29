import tkinter as tk  # python 3
from tkinter import font as tkfont  # python 3
from src.hyperOptimizeApp.view.HomeView import HomeView
from src.hyperOptimizeApp.view.ModelView import ModelView


class ControlFrame(tk.Frame):

    def __init__(self, mainView, main, width, homeView, modelView):
        tk.Frame.__init__(self, main)

        self.changeStyle("black")
        self.place(x=0, y=380, height=100, width=width)

        # Fenster Zeichen
        tk.Button(self, text="Home", command=lambda: showFrame(homeView)).pack()
        tk.Button(self, text="New Model", command=lambda: showFrame(modelView)).pack()
        tk.Button(self, text="Quit", command=mainView.close).pack()

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
        mFile.add_command(label="New Model", command=lambda: showFrame(modelView))
        mFile.add_command(label="Load Model")
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


class MainView:
    main = tk.Tk()

    def __init__(self):
        # Konstanten
        WM_HEIGHT = 480
        WM_WIDTH = 800

        # Hauptfenster

        self.main.title("Test")
        self.main.geometry("{:}x{:}".format(WM_WIDTH, WM_HEIGHT))
        # main.attributes("-fullscreen", True)
        self.main.resizable(0, 0)

        homeView = HomeView(self.main, WM_WIDTH, WM_HEIGHT - 100)
        modelView = ModelView(self.main, WM_WIDTH, WM_HEIGHT - 100)

        ControlFrame(self, self.main, WM_WIDTH, homeView, modelView)

        self.main.mainloop()

    def build(self, text):
        print(text)

    # Function for closing
    def close(self):
        self.main.destroy()


def showFrame(frame):
    frame.tkraise()
