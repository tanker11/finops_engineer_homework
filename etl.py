import sqlite3
import pandas as pd
import json


class LoadService:
    '''
    Handles db and tables creation
    '''
    def __init__(self, local_db_name="loaddata.db", local_json_name="metrics.json"):
        self.local_path = ""
        self.local_db_name = self.local_path+local_db_name
        self.local_json_name = self.local_path+local_json_name
        self.df = pd.DataFrame()
        self.init_db()
        self.load_json()

    def load_json(self):
        self.df = pd.read_json(self.local_json_name)
        print(self.df)

    def init_db(self):
        #Initialize the local SQLite database
        with sqlite3.connect(self.local_db_name) as conn:
            cursor = conn.cursor()
            #Create table for metrics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    warehouse_name TEXT,
                    task_name TEXT,
                    instance_name TEXT,
                    cpu_ms INTEGER
                )
            ''')
            conn.commit()



myservice = LoadService()
