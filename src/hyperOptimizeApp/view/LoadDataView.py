import tkinter as tk  # python 3

from src.hyperOptimizeApp.view.ProjectView import ProjectView


class LoadDataView(tk.Frame):
    controlFrame = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)
        self.topText = tk.StringVar()
        self.topText.set("Load data view.")

    def addControlFrame(self, frame):
        self.controlFrame = frame
