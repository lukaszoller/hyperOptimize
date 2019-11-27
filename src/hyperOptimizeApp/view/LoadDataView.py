import tkinter as tk  # python 3

from src.hyperOptimizeApp.view.ProjectView import ProjectView


class LoadDataView(tk.Frame):
    controlFrame = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)
        # nameLabel = tk.Label(self, text="Project Name").grid(row=1, column=2)

        # path to data
        pathFrame = tk.Frame(self)
        pathFrame.pack(fill=tk.X)
        pathLabel = tk.Label(pathFrame, text="Path to data", width=10)
        pathLabel.pack(side=tk.LEFT, padx=5, pady=5)
        self.entryPath = tk.Entry(pathFrame, width=10)
        self.entryPath.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        getFileLocationBtn = tk.Button(pathFrame, text="Get file location", command=lambda: self.getFileLocation())
        getFileLocationBtn.pack(side=tk.RIGHT, padx=5, pady=5)

        # checkboxes
        checkBtnFrame = tk.Frame(self)
        checkBtnFrame.pack(fill=tk.X)
        firstRowIsTitleCheckBtn = tk.Checkbutton(checkBtnFrame, text="First row is title")
        firstRowIsTitleCheckBtn.pack(side=tk.LEFT, padx=5, pady=5)
        firstColIsRowNbrCheckBtn = tk.Checkbutton(checkBtnFrame, text="First column is row number")
        firstColIsRowNbrCheckBtn.pack(side=tk.LEFT, padx=5, pady=5)

    def addControlFrame(self, frame):
        self.controlFrame = frame


    def getFileLocation(self):
        self.entryPath.delete(0, tk.END)
        self.entryPath.insert(0, tk.filedialog.askopenfilename(filetypes=[('csv Files', '*.csv')]))
        return