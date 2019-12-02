import glob
import sqlite3
import datetime
import tensorflow as tf
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseModelModel import DatabaseModelModel
from src.hyperOptimizeApp.logic.dbInteraction.DatabaseProjectModel import DatabaseProjectModel
from src.hyperOptimizeApp.logic.MachineLearningModel import MachineLearningModel
from src.hyperOptimizeApp.logic.HyperParamsObj import HyperParamsObj
from src.hyperOptimizeApp.logic.LoadDataModel import LoadDataModel


class DatabaseConnector:
    DATABASE_NAME = "project_database.db"

    def __init__(self):
        # create table for projects if not existing:
        if not glob.glob(self.DATABASE_NAME):
            sql = "CREATE TABLE project(id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, date DATE NOT NULL," \
                  "dataPath VARCHAR, firstRowIsTitle INTEGER, firstColIsRowNbr INTEGER, nbrOfFeatures INTEGER, " \
                  "dataIsSet INTEGER NOT NULL)"
            self.writeDB(sql)
            sql = "CREATE TABLE model(id INTEGER PRIMARY KEY, modelName VARCHAR NOT NULL, date DATE NOT NULL, " \
                  "serializedModel VARCHAR NOT NULL, projectId INTEGER, FOREIGN KEY(projectId) REFERENCES project(id))"
            self.writeDB(sql)
        # self.addProject("Project 1")
        # self.addProject("Project 2")
        # self.addProject("Project 3")
        # hyperParams = HyperParamsObj()
        # model = MachineLearningModel(hyperParams)
        # self.saveModel(model, 1)

        # set pathToModels where Models are saved on filesystem
        self.pathToModels = "/savedModels/"

    def getAllProjects(self):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT id, name, dataPath, dataIsSet FROM project"
        cursor.execute(sql)
        projects = []
        for element in cursor:
            print(element[1])
            data = element[3]
            dataIsSet = False
            if data == 1:
                dataIsSet = True
            project = DatabaseProjectModel(element[0], element[1], element[2], dataIsSet)
            projects.append(project)
        connector.close()
        print(projects)
        return projects

    def addProject(self, projectName):
        date = datetime.date.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO project(name, date, dataIsSet) VALUES('" + projectName + "', " + date + ", 0)"
        self.writeDB(sql)

    def getProjectById(self, projectId):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT id, name, dataPath, dataIsSet FROM project WHERE id = {}".format(projectId)
        cursor.execute(sql)
        data = cursor.fetchone()[3]
        dataIsSet = False
        if data == 1:
            dataIsSet = True
        project = DatabaseProjectModel(cursor.fetchone()[0], cursor.fetchone()[1], cursor.fetchone()[2], dataIsSet)
        connector.close()
        return project

    def deleteProjectById(self, projectId):
        sql = "DELETE FROM project WHERE id = {}".format(projectId)
        self.writeDB(sql)

    def updateProject(self, project=DatabaseProjectModel()):
        sql = "UPDATE project SET name = '{}' WHERE id = {}".format(project.projectName, project.projectId)
        self.writeDB(sql)

    def updateProjectDataInformation(self, projectId, dataPath, firstRowIsHeader, firstColIsRowNbr, nbrOfFeatures):
        rowHeader = 0
        colRowNbr = 0
        if firstRowIsHeader:
            rowHeader = 1
        if firstColIsRowNbr:
            colRowNbr = 1
        sql = "UPDATE project SET dataPath = '{}', firstRowIsTitle = {}, firstColIsRowNbr = {}, nbrOfFeatures = {}, " \
              "dataIsSet=1 WHERE id = {}".format(dataPath, rowHeader, colRowNbr, nbrOfFeatures, projectId)
        self.writeDB(sql)

    def getProjectDataInformation(self, projectId):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT dataPath, firstRowIsTitle, firstColIsRowNbr, nbrOfFeatures FROM project WHERE id = {}"\
            .format(projectId)
        cursor.execute(sql)
        rowHeader = cursor.fetchone()[1]
        colRowNbr = cursor.fetchone()[2]
        firstRowIsTitle = False
        if rowHeader == 1:
            firstRowIsTitle = True
        firstColIsRowNbr = False
        if colRowNbr == 1:
            firstColIsRowNbr = True
        dataModel = LoadDataModel(firstRowIsTitle, firstColIsRowNbr, cursor.fetchone()[3], cursor.fetchone()[0])
        return dataModel

    def writeDB(self, sql):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        cursor.execute(sql)
        connector.commit()
        connector.close()

    def saveModel(self, modelName, model, projectId):
        model_json = model.to_json()
        print("saveModel: print model_json: ", model_json)
        date = datetime.date.today().strftime('%Y-%m-%d')
        projectId = str(projectId)
        sql = "INSERT INTO model(modelName, date, serializedModel, projectID) VALUES('" + modelName + "', " + date + \
              ", '" + model_json + "', '" + projectId + "')"
        self.writeDB(sql)

    def getModelByID(self, modelId):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT serializedModel FROM model WHERE id = {}".format(modelId)
        cursor.execute(sql)
        model_json = str(cursor.fetchone())
        print("getModelByID: print model_json: ", model_json)
        model = tf.keras.models.model_from_json(model_json)
        connector.close()
        return model

    def getAllModelsByProjectId(self, projectId):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        models = []
        sql = "SELECT modelName, serializedModel FROM model WHERE projectId = {}".format(projectId)
        cursor.execute(sql)
        for element in cursor:
            # JUST FOR TESTING
            hyperParams = HyperParamsObj()
            model = MachineLearningModel(hyperParams, element[0])
            model.model = tf.keras.models.model_from_json(element[1])
            models.append(model)
        connector.close()
        for model in models:
            print(model.modelName)
        return models

    def deleteModelsByProjectId(self, projectId):
        sql = "DELETE FROM model WHERE projectId = {}".format(projectId)
        self.writeDB(sql)



#Probably not needed (get last project ID)
    # def getMaxId(self):
    #     connector = sqlite3.connect(self.DATABASE_NAME)
    #     cursor = connector.cursor()
    #     sql = "SELECT MAX(id) from project"
    #     cursor.execute(sql)
    #     maxId = int(cursor.fetchone()[0])
    #     connector.close()
    #     return maxId

