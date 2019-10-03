from tkinter import *
from tkinter import ttk
from src.hyperOptimizeApp.view.HomeView import HomeView


class MainView:
    def __init__(self):
        height = 200
        width = 400

        homeView = HomeView()

    def build(self, textboxText):
        main = Tk()
        main.title("Neural Network Optimizer")

        lbl = Label(main, text=textboxText)

        lbl.grid(column=0, row=0)

        main.mainloop()
