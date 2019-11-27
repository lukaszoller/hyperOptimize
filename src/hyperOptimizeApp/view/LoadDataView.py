import tkinter as tk  # python 3

from src.hyperOptimizeApp.view.ProjectView import ProjectView


class LoadDataView(tk.Frame):
    controlFrame = None

    def __init__(self, main, width, height):
        tk.Frame.__init__(self, main)
        padding = 5

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)
        # nameLabel = tk.Label(self, text="Project Name").grid(row=1, column=2)

        # path to data
        pathFrame = tk.Frame(self)
        pathFrame.pack(fill=tk.X)
        pathLabel = tk.Label(pathFrame, text="Path to data", width=10)
        pathLabel.pack(side=tk.LEFT, padx=padding, pady=padding)
        self.entryPath = tk.Entry(pathFrame, width=10)
        self.entryPath.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=padding)
        getFileLocationBtn = tk.Button(pathFrame, text="Get file location", command=lambda: self.getFileLocation())
        getFileLocationBtn.pack(side=tk.RIGHT, padx=padding, pady=padding)

        # checkboxes
        checkBtnFrame = tk.Frame(self)
        checkBtnFrame.pack(fill=tk.X)
        firstRowIsTitleCheckBtn = tk.Checkbutton(checkBtnFrame, text="First row is title")
        firstRowIsTitleCheckBtn.pack(side=tk.LEFT, padx=padding, pady=padding)
        firstColIsRowNbrCheckBtn = tk.Checkbutton(checkBtnFrame, text="First column is row number")
        firstColIsRowNbrCheckBtn.pack(side=tk.LEFT, padx=padding, pady=padding)

        # nbr of features
        nbrFeaturesFrame = tk.Frame(self)
        nbrFeaturesFrame.pack(fill=tk.X)
        nbrFeaturesLabel = tk.Label(nbrFeaturesFrame, text="Input number of features (only positive numbers allowed)",
                                    width=50)
        nbrFeaturesLabel.pack(side=tk.LEFT, padx=padding, pady=padding)
        validation = self.register(self.isPositiveNumber)
        entryNbrFeatures = tk.Entry(nbrFeaturesFrame, width=10, validate="key", validatecommand=(validation, '%S'))
        entryNbrFeatures.pack(fill=tk.X, side=tk.LEFT, padx=padding)
        self.nbrFeaturesWarning = tk.Label(nbrFeaturesFrame, text="")
        self.nbrFeaturesWarning.pack(side=tk.LEFT, padx=padding, pady=padding)

        # Preview data btn
        previewBtnFrame = tk.Frame(self)
        previewBtnFrame.pack(fill=tk.X)
        previewBtn = tk.Button(previewBtnFrame, text="Preview data", command=lambda: self.displayNbrFeaturesWarning())
        previewBtn.pack(side=tk.LEFT,  padx=padding, pady=padding)


        # Preview data table


    def addControlFrame(self, frame):
        self.controlFrame = frame

    def isPositiveNumber(self, inputStr):       # Code for validation from: https://riptutorial.com/tkinter/example/27780/adding-validation-to-an-entry-widget
        if inputStr.isdigit():
            if int(inputStr) > 0:
                return True
        else:
            return False


    def displayNbrFeaturesWarning(self):
        self.nbrFeaturesWarning.config(text="Warning! Enter number which is smaller than number of columns.",
                                       fg="red")


    def getFileLocation(self):
        self.entryPath.delete(0, tk.END)
        self.entryPath.insert(0, tk.filedialog.askopenfilename(filetypes=[('csv Files', '*.csv')]))
        return