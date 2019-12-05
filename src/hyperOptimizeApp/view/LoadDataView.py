import tkinter as tk  # python 3
import tkinter.messagebox
import numpy as np
from src.hyperOptimizeApp.logic.dbInteraction.DataInteractionModel import DataInteractionModel
from src.hyperOptimizeApp.view import LayoutConstants
from src.hyperOptimizeApp.view import ValidationFunctions


class LoadDataView(tk.Frame):
    controlFrame = None
    project = None
    dbInteraction = DataInteractionModel()

    def __init__(self, main, width, height, loadDataModel):
        self.loadDataModel = loadDataModel
        tk.Frame.__init__(self, main)

        self.config(bg="white")
        self.place(relx=0, rely=0, height=height, width=width)
        # nameLabel = tk.Label(self, text="Project Name").grid(row=1, column=2)

        # path to datal
        pathFrame = tk.Frame(self)
        pathFrame.pack(fill=tk.X)
        pathLabel = tk.Label(pathFrame, text="Path to data", width=10)
        pathLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.entryPath = tk.Entry(pathFrame, width=10)
        self.entryPath.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=LayoutConstants.PADDING)
        getFileLocationBtn = tk.Button(pathFrame, text="Get file location", command=lambda: self.getFileLocation())
        getFileLocationBtn.pack(side=tk.RIGHT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # checkboxes
        checkBtnFrame = tk.Frame(self)
        checkBtnFrame.pack(fill=tk.X)
        self.checkVarRow = tk.IntVar()
        firstRowIsTitleCheckBtn = tk.Checkbutton(checkBtnFrame, text="First row is title", variable=self.checkVarRow)
        firstRowIsTitleCheckBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.checkVarCol = tk.IntVar()
        firstColIsRowNbrCheckBtn = tk.Checkbutton(checkBtnFrame, text="First column is row number", variable=self.checkVarCol)
        firstColIsRowNbrCheckBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # nbr of categories
        nbrCategoriesFrame = tk.Frame(self)
        nbrCategoriesFrame.pack(fill=tk.X)
        nbrCategoriesLabel = tk.Label(nbrCategoriesFrame, text="Input number of categories (only positive numbers allowed)",
                                    width=50)
        nbrCategoriesLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        nbrCategoriesValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entryNbrCategories = tk.Entry(nbrCategoriesFrame, width=10, validate="key", validatecommand=(nbrCategoriesValidation, '%S'))
        self.entryNbrCategories.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.nbrCategoriesWarning = tk.Label(nbrCategoriesFrame, text="")
        self.nbrCategoriesWarning.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # training data starts at linenbr
        trainRowNbrFrame = tk.Frame(self)
        trainRowNbrFrame.pack(fill=tk.X)
        trainRowNbrLabel = tk.Label(trainRowNbrFrame,
                                      text="Input row number where training data starts",
                                      width=50)
        trainRowNbrLabel.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        trainRowNbrValidation = self.register(ValidationFunctions.isPositiveNumber)
        self.entrytrainRowNbr = tk.Entry(trainRowNbrFrame, width=10, validate="key",
                                           validatecommand=(trainRowNbrValidation, '%S'))
        self.entrytrainRowNbr.pack(fill=tk.X, side=tk.LEFT, padx=LayoutConstants.PADDING)
        self.trainRowNbrWarning = tk.Label(trainRowNbrFrame, text="")
        self.trainRowNbrWarning.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Load data btn
        dataBtnFrame = tk.Frame(self)
        dataBtnFrame.pack(fill=tk.X)
        loadDataBtn = tk.Button(dataBtnFrame, text="Load data", command=lambda: self.loadPreviewData())
        loadDataBtn.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)
        self.loadDataInformation = tk.Label(dataBtnFrame, text="")
        self.loadDataInformation.pack(side=tk.LEFT, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

        # Set data btn
        setDataBtn = tk.Button(dataBtnFrame, text="Set data", command=lambda: self.setData())
        setDataBtn.pack(side=tk.LEFT)


        # Preview data table
        previewDataFrame = tk.Frame(self)
        previewDataFrame.pack(fill=tk.X)
        self.preViewDataText = tk.Text(previewDataFrame)
        self.preViewDataText.pack(side=tk.LEFT, expand=True, padx=LayoutConstants.PADDING, pady=LayoutConstants.PADDING)

    def addControlFrame(self, frame):
        self.controlFrame = frame

    def displayNbrInputWarning(self):
        self.nbrCategoriesWarning.config(text="Warning! Enter number smaller than number of columns.", fg="red")

    def getFileLocation(self):
        self.entryPath.delete(0, tk.END)
        self.entryPath.insert(0, tk.filedialog.askopenfilename(filetypes=[('csv Files', '*.csv')]))
        return

    def loadPreviewData(self):
        """Runs loadData from LoadDataModel. Runs also previewData from this class. Shows error warning in GUI if data
        load does not work."""
        # parameters for data load from GUI
        self.loadDataModel.pathToDataSet = self.entryPath.get()
        self.loadDataModel.firstRowIsTitle = bool(self.checkVarRow.get())
        self.loadDataModel.firstColIsRowNbr = bool(self.checkVarCol.get())
        # if entry field is empty, set nbrOfCategories to 0
        if len(self.entrytrainRowNbr.get()) == 0:  # Code for this line from: https://stackoverflow.com/questions/15455113/tkinter-check-if-entry-box-is-empty
            self.loadDataModel.trainRowNumber = 0
        else:
            self.loadDataModel.trainRowNumber = int(self.entrytrainRowNbr.get())
        # if entry field is empty, set nbrOfCategories to 0
        if len(
                self.entryNbrCategories.get()) == 0:  # Code for this line from: https://stackoverflow.com/questions/15455113/tkinter-check-if-entry-box-is-empty
            self.loadDataModel.nbrOfCategories = 0
        else:
            self.loadDataModel.nbrOfCategories = int(self.entryNbrCategories.get())
        self.loadDataModel.dataIsForTraining = True

        # Load data
        try:
            self.loadDataModel.loadData()
            print("LoadDataView: self.loadDataModel.data: ", self.loadDataModel.data)
        except FileNotFoundError:
            tk.messagebox.showerror("Error", " File not found.")
        except ValueError:
            tk.messagebox.showerror("Error", "The number of categories entered is incorrect. Enter number > 0 and smaller"
                                             " the number of columns in the dataset.")
        except:
            print("Load data failed because of something different than nbrOfCategories entered or file not found.")
        else:  # if data load worked do the following
            self.loadDataInformation.config(text="Data has been successfully loaded and stored.", fg="green")
            self.previewData()

    def setData(self):
        # Check if load Data model has been set
        msg = ""
        if self.loadDataModel.pathToDataSet == None:
            msg = msg + "pathToDataSet parameter not correctly stored.\n"
        if self.loadDataModel.firstRowIsTitle == None:
            msg = msg + "firstRowIsTitle not correctly stored.\n"
        if self.loadDataModel.firstColIsRowNbr == None:
            msg = msg + "firstColIsRowNbr parameter not correctly stored.\n"
        if self.loadDataModel.trainRowNumber == None:
            msg = msg + "trainRowNumber parameter not correctly stored.\n"
        if self.loadDataModel.nbrOfCategories == None:
            msg = msg + "nbrOfCategories parameter not correctly stored.\n"
        if self.loadDataModel.dataIsForTraining == None:
            msg = msg + "dataIsForTraining not correctly stored.\n"
        # Give Warning if
        if msg != "":
            msg = msg + "\nData has to be loaded correctly before leaving this window."
            tk.messagebox.showwarning("Data not correctly stored", msg)
            return

        answer = tk.messagebox.askyesno("Confirm deletion", "Are you sure to set Data?\n"
                                                            "This process can't be reversed!")
        if answer == 1:
            print("Leave Window and disable Data load Button in Project View.")
        else:
            print("Nothing done")

    def previewData(self):
        """Previews loaded data."""
        x, y, rawData = self.loadDataModel.data
        shapeRaw = np.shape(rawData)
        nbrOfCols = shapeRaw[1]
        data = rawData[0:100, 0:nbrOfCols]
        self.preViewDataText.delete('1.0', tk.END)
        self.preViewDataText.insert(tk.INSERT, data)


    def displayPreviewWarning(self):
        self.loadDataInformation.config(text="Warning! Data cannot be previewed!", fg="red")

    def setProject(self, project):
        self.project = project
