import pyodbc
from s3_project.Config.config_manager import find_variable
from s3_project.functions import create_table_schema
import ast
import json


class ProjectDatabase:
    def __init__(self):
        self.server = '35.179.41.219'
        self.database = 'SpartaGlobal'
        self.username = 'SA'
        self.password = 'Passw0rd2018'
        self.connection_string = "DRIVER={SQL Server};"
        self.connection_string += f"SERVER={self.server};"
        self.connection_string += f"DATABASE={self.database};"
        self.connection_string += f"UID={self.username};"
        self.connection_string += f"PWD={self.password}"
        self.sparta = pyodbc.connect(self.connection_string)
        self.cursor = self.sparta.cursor()
        self.tables = []
        self.schemas = []
        self.get_schemas()
        self.create_jsons()

    def _sql_query(self, sql_query):
        return self.cursor.execute(sql_query)

    def create_table_no_keys(self):
        # Creates a table without any primary or foreign keys from a dictionary containing the table dictionaries
        all_lines = []
        for table in self.tables:
            schema = table['Schema']
            columns = schema.keys()
            for column in columns:
                all_lines.append(f"{column} {schema[column]['variable type']} {schema[column]['if null']}")
        query = f"""
                USE SpartaGlobal
                CREATE TABLE {table['Name']}
                (
                """
        query += ',\n'.join(all_lines)
        query += ');'
        print(query)
        self._sql_query(query)
        self.sparta.commit()

    def get_schemas(self):
        tables = find_variable('all_tables', 'TABLE SCHEMAS').split(',')
        for table in tables:
            self.tables.append({'Name': table, 'Schema': ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))})

    def create_jsons(self):
        for table in self.tables:
            self.schemas.append(table['Schema'])
            create_table_schema(table, 'database_schema.json')

new = ProjectDatabase()
new.create_table_no_keys()
