import tkinter as tk  # python 3
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

        # path to datal
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

        # Load and preview data btn
        loadPreviewDataFrame = tk.Frame(self)
        loadPreviewDataFrame.pack(fill=tk.X)
        loadPreviewDataBtn = tk.Button(loadPreviewDataFrame, text="Preview data", command=lambda: self.loadPreviewData())
        loadPreviewDataBtn.pack(side=tk.LEFT,  padx=padding, pady=padding)
        self.loadDataInformation = tk.Label(loadPreviewDataFrame, text="")
        self.loadDataInformation.pack(side=tk.LEFT, padx=padding, pady=padding)

        # Preview data table
        previewDataFrame = tk.Frame(self)
        previewDataFrame.pack(fill=tk.X)
        self.preViewDataText = tk.Text(previewDataFrame)
        self.preViewDataText.pack(side=tk.LEFT, expand=True, padx=padding, pady=padding)

        # Load data to project
        loadPreviewDataFrame = tk.Frame(self)
        loadPreviewDataFrame.pack(fill=tk.X)
        loadPreviewDataBtn = tk.Button(loadPreviewDataFrame, text="Assign data to model", command=lambda: self.assignDataToProject())
        loadPreviewDataBtn.pack(side=tk.LEFT, padx=padding, pady=padding)

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

    def loadPreviewData(self):
        """Runs loadData from LoadDataModel. Runs also previewData from this class. Shows error warning in GUI if data
        load does not work."""
        # parameters for data load from GUI
        pathToData = self.entryPath.get()
        firstRowIsHeader = bool(self.checkVarRow.get())
        firstColIsRownbr = bool(self.checkVarCol.get())
        # if entry field is empty, set nbrOfCategories to 0
        if len(
                self.entryNbrCategories.get()) == 0:  # Code for this line from: https://stackoverflow.com/questions/15455113/tkinter-check-if-entry-box-is-empty
            nbrOfCategories = 0
        else:
            nbrOfCategories = int(self.entryNbrCategories.get())
        dataIsForTraining = True

        # Load data
        try:
            self.loadDataModel.loadPreviewData(pathToData, firstRowIsHeader, firstColIsRownbr, nbrOfCategories, dataIsForTraining)
            print("LoadDataView: self.loadDataModel.data: ", self.loadDataModel.data)
        except FileNotFoundError:
            tk.messagebox.showerror("Error", " File not found.")
        except ValueError:
            tk.messagebox.showerror("Error", "The number of categories entered is incorrect. Enter number > 0 and smaller"
                                             " the number of columns in the dataset.")
        except:
            print("Load data failed because of something different than nbrOfCategories entered or file not found.")
        else:  # if data load worked do the following
            self.loadDataInformation.config(text="Data has been successfully read from file.", fg="green")
            self.previewData()

    def previewData(self):
        """Previews loaded data."""
        x, y, rawData = self.loadDataModel.data
        self.preViewDataText.delete(1, tk.END)
        self.preViewDataText.insert(tk.END, rawData)

    def displayPreviewWarning(self):
        self.loadDataInformation.config(text="Warning! Data cannot be previewed!", fg="red")

    def assignDataToProject(self):
        """Data is already loaded. This method closes the load window which won't be accessible later."""