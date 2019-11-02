import datetime
import glob
import sqlite3

from src.hyperOptimizeApp.logic.ProjectModel import ProjectModel


class ProjectDatabase:
    DATABASE_NAME = "project_database.db"

    def __init__(self):
        # create table for projects if not existing:
        if not glob.glob(self.DATABASE_NAME):
            connector = sqlite3.connect(self.DATABASE_NAME)
            cursor = connector.cursor()
            sql = "CREATE TABLE project(id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, date DATE NOT NULL)"
            cursor.execute(sql)
            connector.close()
        self.addProject("Project 1")
        self.addProject("Project 2")
        self.addProject("Project 3")

    def getAllProjects(self):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT * FROM project"
        cursor.execute(sql)
        projects = []
        for element in cursor:
            print(element[1])
            project = ProjectModel(element[1], element[2], [])
            projects.append(project)
        connector.close()
        print(projects)
        return projects

    def addProject(self, name):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        date = datetime.date.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO project(name, date) VALUES('{}', '{}')".format(name, str(date))
        print(sql)
        cursor.execute(sql)
        connector.close()
