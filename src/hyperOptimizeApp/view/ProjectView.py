import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfile

from src.hyperOptimizeApp.persistence.SaverLoader import SaverLoader


def openFile():
    saverLoader = SaverLoader()
    file = askopenfile(mode='r', filetypes=[('csv Files', '*.csv')])
    if file is not None:
        saverLoader.setFileName(file.name)
        print(saverLoader.getEstTimeData())


class ProjectView(tk.Frame):

    controlFrame = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)
        self.topText = tk.StringVar()
        self.topText.set("Project")

        topLabel = tk.Label(self, textvariable=self.topText).pack(side=tk.TOP)

        self.config(bg="grey")
        self.place(relx=0, rely=0, height=height, width=width)
        loadFileButton = tk.Button(self, text='Open', command=lambda: openFile())
        loadFileButton.pack(side=tk.TOP, pady=10)

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def setTopText(self, text):
        self.topText.set(text)
