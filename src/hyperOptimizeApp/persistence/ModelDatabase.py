import sqlite3, glob

class ModelDatabase:
    DATABASE_NAME = "model_database.db"

    def __init__(self):
        # create table for models if not existing:
        if not glob.glob(self.DATABASE_NAME):
            connector = sqlite3.connect(self.DATABASE_NAME)
            cursor = connector.cursor()
            sql = "CREATE TABLE model(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50) NOT NULL, date DATE NOT NULL)"
            cursor.execute(sql)
            connector.close()

    def getAllModels(self):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        sql = "SELECT name, date FROM model ORDER BY DATE DESC"
        return cursor.execute(sql)
        connector.close()

    def addModel(self, name):
        connector = sqlite3.connect(self.DATABASE_NAME)
        cursor = connector.cursor()
        #TODO: Add correct statement.
        #sql = "INSERT INTO model VALUES(NULL, NULL)"
        #cursor.execute(sql)
        connector.close()