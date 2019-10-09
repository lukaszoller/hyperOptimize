import tkinter as tk  # python 3
from tkinter import font as tkfont  # python 3
from src.hyperOptimizeApp.view.HomeView import HomeView
from src.hyperOptimizeApp.view.ModelView import ModelView


class ControlFrame(tk.Frame):

    def __init__(self, main, width, homeView, modelView):
        tk.Frame.__init__(self, main)

        self.config(bg="grey")
        self.place(x=0, y=380, height=100, width=width)

        # Fenster Zeichen
        tk.Button(self, text="Main", command=lambda: showFrame(homeView)).pack()
        tk.Button(self, text="Home", command=lambda: showFrame(modelView)).pack()


class MainView:

    def __init__(self):
        # Konstanten
        WM_HEIGHT = 480
        WM_WIDTH = 800

        # Hauptfenster

        main = tk.Tk()
        main.title("Test")
        main.geometry("{:}x{:}".format(WM_WIDTH, WM_HEIGHT))
        # main.attributes("-fullscreen", True)
        main.resizable(0, 0)

        homeView = HomeView(main, WM_WIDTH, WM_HEIGHT - 100)
        modelView = ModelView(main, WM_WIDTH, WM_HEIGHT - 100)

        ControlFrame(main, WM_WIDTH, homeView, modelView)

        main.mainloop()

    def build(self, text):
        print(text)

def showFrame(frame):
    frame.tkraise()