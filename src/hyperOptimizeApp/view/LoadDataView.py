import tkinter as tk  # python 3

from src.hyperOptimizeApp.view.ProjectView import ProjectView


class LoadDataView(tk.Frame):
    controlFrame = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)
        nameLabel = tk.Label(self, text="Project Name").grid(row=1, column=2)


    def addControlFrame(self, frame):
        self.controlFrame = frame
