import tkinter as tk  # python 3
from tkintertable import TableCanvas, TableModel
import numpy as np

class LoadDataView(tk.Frame):
    controlFrame = None

    def __init__(self, main, width, height, loadDataModel):
        self.loadDataModel = loadDataModel
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
        self.checkVarRow = tk.IntVar()
        firstRowIsTitleCheckBtn = tk.Checkbutton(checkBtnFrame, text="First row is title", variable=self.checkVarRow)
        firstRowIsTitleCheckBtn.pack(side=tk.LEFT, padx=padding, pady=padding)
        self.checkVarCol = tk.IntVar()
        firstColIsRowNbrCheckBtn = tk.Checkbutton(checkBtnFrame, text="First column is row number", variable=self.checkVarCol)
        firstColIsRowNbrCheckBtn.pack(side=tk.LEFT, padx=padding, pady=padding)

        # nbr of categories
        nbrCategoriesFrame = tk.Frame(self)
        nbrCategoriesFrame.pack(fill=tk.X)
        nbrCategoriesLabel = tk.Label(nbrCategoriesFrame, text="Input number of categories (only positive numbers allowed)",
                                    width=50)
        nbrCategoriesLabel.pack(side=tk.LEFT, padx=padding, pady=padding)
        nbrCategoriesValidation = self.register(self.isPositiveNumber)
        self.entryNbrCategories = tk.Entry(nbrCategoriesFrame, width=10, validate="key", validatecommand=(nbrCategoriesValidation, '%S'))
        self.entryNbrCategories.pack(fill=tk.X, side=tk.LEFT, padx=padding)
        self.nbrCategoriesWarning = tk.Label(nbrCategoriesFrame, text="")
        self.nbrCategoriesWarning.pack(side=tk.LEFT, padx=padding, pady=padding)

        # Preview data btn
        previewBtnFrame = tk.Frame(self)
        previewBtnFrame.pack(fill=tk.X)
        previewBtn = tk.Button(previewBtnFrame, text="Preview data", command=lambda: self.previewData())
        previewBtn.pack(side=tk.LEFT,  padx=padding, pady=padding)
        self.previewWarning = tk.Label(previewBtnFrame, text="")
        self.previewWarning.pack(side=tk.LEFT, padx=padding, pady=padding)

        # Preview data table
        self.previewTableFrame = tk.Frame(self)
        self.previewTableFrame.pack(fill=tk.X)

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def isPositiveNumber(self, inputStr):       # Code for validation from: https://riptutorial.com/tkinter/example/27780/adding-validation-to-an-entry-widget
        if inputStr.isdigit():
            if int(inputStr) > 0:
                return True
        else:
            return False


    def displayNbrCategoriesWarning(self):
        self.nbrCategoriesWarning.config(text="Warning! Enter number smaller than number of columns.", fg="red")


    def getFileLocation(self):
        self.entryPath.delete(0, tk.END)
        self.entryPath.insert(0, tk.filedialog.askopenfilename(filetypes=[('csv Files', '*.csv')]))
        return

    def previewData(self):
        print("LoadDataView.previewData() executed", self.entryPath.get())
        """Loads data to preview from loadDataModel, reduces the shown area of the data and creates a table with the
        preview data."""
        maxRownbrToShow = 30
        maxColnbrToShow = 100
        # load data
        pathToData = self.entryPath.get()
        firstRowIsHeader = bool(self.checkVarRow.get())
        firstColIsRownbr = bool(self.checkVarCol.get())
        # if entry field is empty, set to 0
        if len(self.entryNbrCategories.get()) == 0:     # Code for this line from: https://stackoverflow.com/questions/15455113/tkinter-check-if-entry-box-is-empty
            nbrOfCategories = 0
        else: nbrOfCategories = self.entryNbrCategories.get()
        dataIsForTraining = True

        print("LoadDataview: nbrOfCategories", nbrOfCategories)

        try:
            data = self.loadDataModel.loadData(pathToData, firstRowIsHeader, firstColIsRownbr, nbrOfCategories, dataIsForTraining)
            dataShape = np.shape(data)
            rows = 0
            # get shape for smallerData
            if dataShape[0] < maxRownbrToShow:
                rows = dataShape[0]
            else:
                rows = maxRownbrToShow

            if dataShape[1] < maxColnbrToShow:
                cols = dataShape[1]
            else:
                cols = maxColnbrToShow

            smallerData = data[0:rows, 0:cols]
            print(smallerData)

            self.previewTable = TableCanvas(self.previewTableFrame, editable=False, data=smallerData)
            self.previewTable.show()
        except ValueError:
            tk.messagebox.showerror("Error", "The number of categories entered is incorrect. Enter number > 0 and smaller"
                                             " the number of columns in the dataset.")


    def displayPreviewWarning(self):
        self.previewWarning.config(text="Warning! Data cannot be previewed!", fg="red")