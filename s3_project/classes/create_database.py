import pyodbc
from
from s3_project.functions import create_table_schema


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
        self.tables = find_variable

    def _sql_query(self, sql_query):
        return self.cursor.execute(sql_query)

    def create_table_no_keys(self, table_name, table_dict):
        # Creates a table without any primary or foreign keys from a dictionary containing the table dictionaries
        all_lines = []
        for column in table_dict:
            all_lines.append(f"{column} {table_dict[column][0]} {table_dict[column][1]}")
        query = f"""
                USE SpartaGlobal
                CREATE TABLE {table_name}
                (
                """
        query += ',\n'.join(all_lines)
        query += ');'
        self._sql_query(query)
        self.sparta.commit()




# new = ProjectDatabase()
# new.create_table_no_keys('Location', {
#                                     'LocationID': {'variable type': 'INT', 'if null': 'NOT NULL'},
#                                     'LocationName': {'variable type': 'VARCHAR(25)', 'if null': 'NOT NULL'}
#                                      })


