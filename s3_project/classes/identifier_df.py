import pandas as pd
import pyodbc
import urllib
import ast
from sqlalchemy import create_engine

from s3_project.classes.joining_class import merged_dfs
from s3_project.Config.config_manager import find_hidden_variable
from s3_project.Config.config_manager import find_variable

class IdentifierDF:
    def __init__(self):
        self.df = merged_dfs.merged_df
        self.Cities = self.df[['city']]
        self.Course_Interests = self.df[['course_interest']]
        self.Courses = self.df[['course_name', 'course_start_date', 'course_length']]
        self.Degrees = self.df[['degree']]
        self.Locations = self.df[['location']]
        self.Staff_Roles = pd.DataFrame({'role': ['Trainer', 'Talent']})
        self.Strengths = self.df[['strengths']]
        self.Universities = self.df[['uni']]
        self.Weaknesses = self.df[['weaknesses']]
        self.server = find_hidden_variable('server')
        self.database = find_hidden_variable('database')
        self.username = find_hidden_variable('username')
        self.password = find_hidden_variable('password')
        self.connection_string = "DRIVER={SQL Server};"
        self.connection_string += f"SERVER={self.server};"
        self.connection_string += f"DATABASE={self.database};"
        self.connection_string += f"UID={self.username};"
        self.connection_string += f"PWD={self.password}"
        self.sparta = pyodbc.connect(self.connection_string)
        self.cursor = self.sparta.cursor()
        self.params = urllib.parse.quote_plus(self.connection_string)
        self.engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % self.params)
        self.input_tables_to_sql()
        self.apply_reassign()

    def _sql_query(self, sql_query):
        return self.cursor.execute(sql_query)

    # This method writes the df to the SQL database
    def df_to_sql(self, df, sql_table):
        df.to_sql(sql_table, con=self.engine, index=False, if_exists='append', chunksize=1000)

    # This method gets the ID's from the database for later use
    def get_id(self, sql_id, sql_column_name, table):
        fk_key_dict = {}
        query = f"SELECT {sql_id}, {sql_column_name} FROM {table};"
        for index, value in self._sql_query(query):
            fk_key_dict[value] = index
        return fk_key_dict

    # This method returns unique items from a column which only contains lists
    def values_from_list(self, column_name, df):
        df_notnull = df[df[column_name].notna()]
        list_append = []
        for each in df_notnull[column_name]:
            for item in each:
                if item not in list_append:
                    list_append.append(item)
        return list_append

    # This method returns a identifier table for columns that have lists and ensures they are unique in the database
    def identifier_list_tables(self, sql_id, sql_column_name, df_column_name, df, table):
        unique_values = self.values_from_list(df_column_name, df)
        column_name_dict = self.get_id(sql_id, sql_column_name, table)
        unique_values = pd.Series(unique_values)
        for index, each in unique_values.iteritems():
            if each in column_name_dict.keys():
                unique_values = unique_values.drop(index=index)
        id_df = pd.DataFrame(unique_values, columns=[sql_column_name])
        return id_df

    # This method creates a dataframes for a column and ensures they are only unique values
    def identifier_df(self, sql_id, sql_column_name, df_column_name, df, table):
        df_notnull = df[df[df_column_name].notna()]
        unique_values = df_notnull.drop_duplicates([df_column_name])
        column_name_dict = self.get_id(sql_id, sql_column_name, table)
        unique_values = unique_values.reset_index(drop=True)
        unique_series = unique_values[df_column_name]
        for index, each in unique_series.iteritems():
            if each in column_name_dict.keys():
                unique_values = unique_values.drop(index=index)
        id_df = pd.DataFrame(unique_values)
        column_keys = find_variable(table, 'TABLE SCHEMAS')
        column_keys = list(ast.literal_eval(column_keys).keys())
        df_keys = df.columns
        column_map_dict = {}
        for i in range(len(df_keys)):
            column_map_dict[df_keys[i]] = column_keys[i+1]
        id_df = id_df.rename(columns=column_map_dict)
        return id_df

    # This loads all the data to SQL
    def input_tables_to_sql(self):
        id_tables = ['Locations', 'Universities', 'Degrees', 'Course_Interests', 'Cities', 'Courses', 'Staff_Roles', 'Strengths', 'Weaknesses']
        df_list = [self.Locations, self.Universities, self.Degrees, self.Course_Interests, self.Cities, self.Courses, self.Staff_Roles, self.Strengths, self.Weaknesses]
        for i in range(len(id_tables)):
            column_keys = find_variable(id_tables[i], 'TABLE SCHEMAS')
            column_keys = list(ast.literal_eval(column_keys).keys())
            df = df_list[i]
            df_column = df.columns[0]
            sql_id = column_keys[0]
            sql_column = column_keys[1]
            if id_tables[i] == 'Strengths' or id_tables[i] == 'Weaknesses':
                id_df = self.identifier_list_tables(sql_id, sql_column, df_column, df, id_tables[i])
                print(f"Loading {id_tables[i]} table into database")
                self.df_to_sql(id_df, id_tables[i])
            else:
                id_df = self.identifier_df(sql_id, sql_column, df_column, df, id_tables[i])
                print(f"Loading {id_tables[i]} table into database")
                self.df_to_sql(id_df, id_tables[i])
        print('9 tables have loaded.')

    # This method reads the keys from the database and maps onto a column
    def reassign_values(self, sql_id, sql_column, df_column, df, table):
        id_dict = self.get_id(sql_id, sql_column, table)
        df[df_column] = df[df_column].map(id_dict)
        df = df.rename(columns={df_column: sql_id})
        return df

    # This methods reassigns every element in the weaknesses column to foreign keys
    def reassign_weaknesses(self, df_column):
        id_dict = self.get_id('keyword_id', 'keyword', 'Weaknesses')
        list_of_keywords = []
        if type(df_column) is not float:
            for item in df_column:
                value = id_dict.get(item)
                list_of_keywords.append(value)
        return list_of_keywords

    # This methods reassigns every element in the strengths column to foreign keys
    def reassign_strengths(self, df_column):
        id_dict = self.get_id('keyword_id', 'keyword', 'Strengths')
        list_of_keywords = []
        if type(df_column) is not float:
            for item in df_column:
                value = id_dict.get(item)
                list_of_keywords.append(value)
        return list_of_keywords

    # This method reads the keys from the database and assigns the foreign key value to the appropriate columns
    def apply_reassign(self):
        print('Reassigning values in dataframe')
        self.df = self.reassign_values('location_id', 'location', 'location', self.df, 'Locations')
        self.df = self.reassign_values('city_id', 'city', 'city', self.df, 'Cities')
        self.df = self.reassign_values('course_type_id', 'course_type', 'course_interest', self.df, 'Course_Interests')
        self.df = self.reassign_values('course_id', 'course_name', 'course_name', self.df, 'Courses')
        self.df = self.reassign_values('degree_id', 'degree', 'degree', self.df, 'Degrees')
        self.df = self.reassign_values('uni_id', 'uni', 'uni', self.df, 'Universities')
        self.df['strengths'] = self.df['strengths'].apply(self.reassign_strengths)
        self.df['weaknesses'] = self.df['weaknesses'].apply(self.reassign_weaknesses)
        print('')


testing = IdentifierDF()