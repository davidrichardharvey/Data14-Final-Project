import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine
from s3_project.classes.talent_csv_cleaning import monthly_talent_info
from s3_project.Config.config_manager import find_hidden_variable


class IdentifierDF:
    def __init__(self):
        self.all_data = monthly_talent_info.df_talent_csv
        # self.server = find_hidden_variable('server')
        # self.database = find_hidden_variable('database')
        # self.username = find_hidden_variable('username')
        # self.password = find_hidden_variable('password')
        # self.connection_string = "DRIVER={SQL Server};"
        # self.connection_string += f"SERVER={self.server};"
        # self.connection_string += f"DATABASE={self.database};"
        # self.connection_string += f"UID={self.username};"
        # self.connection_string += f"PWD={self.password}"
        # self.sparta = pyodbc.connect(self.connection_string)
        # self.cursor = self.sparta.cursor()
        self.params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;DATABASE=Project;")
        self.engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % self.params)

        # self.degrees = self.identifier_df('degree', self.all_data)
        # self.uni = self.identifier_df('uni', self.all_data)
        # self.location = self.identifier_df('location', self.all_data)

    def _sql_query(self, sql_query):
        return self.cursor.execute(sql_query)

    def identifier_df(self, column_name, df, table):
        df_notnull = df[df[column_name].notna()]
        unique_values = pd.unique(df_notnull[column_name])
        column_name_dict = self.get_id(column_name, table)
        for index, each in unique_values.iteritems():
            if each in column_name_dict:
                unique_values = unique_values.drop(index=index)
        id_df = pd.DataFrame(unique_values, columns=column_name)
        return id_df

    def df_to_sql(self, df, sql_table):
        df.to_sql(sql_table, con=self.engine, index=False, if_exists='append', chunksize=1000)

    def get_id(self, column_name, table):
        fk_key_dict = {}
        query = f"SELECT {column_name}_id, {column_name} FROM {table};"
        for index, value in self._sql_query(query):
            fk_key_dict[value] = index
        return fk_key_dict

    def assign_fk(self, column_name, id_dict):
        self.all_data[column_name] = self.all_data[column_name].map(id_dict)



testing = IdentifierDF()
testing.

