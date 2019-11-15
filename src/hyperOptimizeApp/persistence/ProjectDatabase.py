import glob
import sqlite3
import datetime

from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel


class ProjectDatabase:
    DATABASE_NAME = "project_database.db"

    def __init__(self):
        # create table for projects if not existing:
        if not glob.glob(self.DATABASE_NAME):
            sql = "CREATE TABLE project(id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, date DATE NOT NULL)"
            self.writeDB(sql)
        # self.addProject("Project 1")
        # self.addProject("Project 2")
        # self.addProject("Project 3")

        # set pathToModels where Models are saved on filesystem
        self.pathToModels = "/savedModels/"

    def getAllProjects(self):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT * FROM project"
        cursor.execute(sql)
        projects = []
        for element in cursor:
            print(element[1])
            project = ProjectModel(element[0], element[1], element[2], [])
            projects.append(project)
        connector.close()
        print(projects)
        return projects

    def addProject(self, name):
        date = datetime.date.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO project(name, date) VALUES('" + name + "', " + date + ")"
        self.writeDB(sql)

    def getProjectById(self, projectId):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT * FROM project WHERE id = {}".format(projectId)
        cursor.execute(sql)
        project = ProjectModel(cursor.fetchone()[0], cursor.fetchone()[1], cursor.fetchone()[2], [])
        connector.close()
        return project

    def deleteProjectById(self, projectId):
        sql = "DELETE FROM project WHERE id = {}".format(projectId)
        self.writeDB(sql)

    def updateProject(self, project=ProjectModel):
        sql = "UPDATE project SET name = {} WHERE id = {}".format(project.projectName, project.projectId)
        self.writeDB(sql)

    def writeDB(self, sql):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        cursor.execute(sql)
        connector.commit()
        connector.close()

    def saveModel(self, projectID, model):
        pathToModels = self.pathToModels
        time = datetime.now()
        sql = "INSERT INTO model(projectID, time, pathToModels) VALUES(" + projectID + ", " + time + ", " + pathToModels + ")"
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

