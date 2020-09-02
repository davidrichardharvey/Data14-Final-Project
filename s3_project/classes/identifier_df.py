import pandas as pd
import pyodbc
import urllib
from sqlalchemy import create_engine

#from s3_project.classes.talent_csv_cleaning import monthly_talent_info
#from s3_project.classes.applicant_info_class import talent_applicant_info
from s3_project.classes.academy_class import academy_dataframe
#from s3_project.classes.cleaning_txt import talent_txt
from s3_project.Config.config_manager import find_hidden_variable


class IdentifierDF:
    def __init__(self):
        #self.df = monthly_talent_info.df_talent_csv
        #self.df = talent_applicant_info.df_talent_json
        #self.df = df = pd.read_pickle('applicant_info.pkl')
        self.df = academy_dataframe.cleaned_df
        # self.server = find_hidden_variable('server')
        # self.database = find_hidden_variable('database')
        # self.username = find_hidden_variable('username')
        # self.password = find_hidden_variable('password')
        # self.connection_string = "DRIVER={SQL Server};"
        # self.connection_string += f"SERVER={self.server};"
        # self.connection_string += f"DATABASE={self.database};"
        # self.connection_string += f"UID={self.username};"
        # self.connection_string += f"PWD={self.password}"
        self.sparta = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;DATABASE=Project;")
        self.cursor = self.sparta.cursor()
        self.params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;DATABASE=Project;")
        self.engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % self.params)

    def _sql_query(self, sql_query):
        return self.cursor.execute(sql_query)

    # This method writes the df to the SQL database
    def df_to_sql(self, df, sql_table):
        df.to_sql(sql_table, con=self.engine, index=False, if_exists='append', chunksize=1000)

    def apply_all(self, sql_id, sql_column, df_column, df, table):
        id_dict = self.get_id(sql_id, sql_column, table)
        df[df_column] = df[df_column].map(id_dict)
        df = df.rename(columns={df_column: sql_id})
        return df

    def get_id(self, sql_id, sql_column_name, table):
        fk_key_dict = {}
        query = f"SELECT {sql_id}, {sql_column_name} FROM {table};"
        for index, value in self._sql_query(query):
            fk_key_dict[value] = index
        return fk_key_dict

    # This method returns unique items from a column which only contains lists
    def values_from_list(self, column_name, df):
        list_append = []
        for each in df[column_name]:
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

    # This returns a data-frame for identifier tables using a specified column and also checks that the values are
    # unique in the database
    def identifier_df(self, sql_id, sql_column_name, df_column_name, df, table):
        df_notnull = df[df[df_column_name].notna()]
        unique_values = pd.unique(df_notnull[df_column_name])
        column_name_dict = self.get_id(sql_id, sql_column_name, table)
        unique_values = pd.Series(unique_values)
        for index, each in unique_values.iteritems():
            if each in column_name_dict.keys():
                unique_values = unique_values.drop(index=index)
        id_df = pd.DataFrame(unique_values, columns=[sql_column_name])
        return id_df

    # This method inputs all the data for identifier tables into the SQL database
    def input_sql_tables(self):
        df = self.df
        course_df = self.df[['course_name', 'course_start_date']]
        # list_of_tables = [['location_id', 'location', 'location', 'Locations'],
        #                   ['course_type_id', 'course_type', 'course_interest', 'Course_Interests'],
        #                   ['degree_id', 'degree', 'degree', 'Degrees'],
        #                   ['uni_id', 'uni', 'uni', 'Universities'],
        #                   ['city_id', 'city', 'city', 'Cities'],
        #                   ['role_id', 'role', 'role', 'Staff_Roles']
        #                   ]
        # strengths_weaknesses = [['keyword_id', 'keyword', 'strengths', 'Strengths'],
        #                         ['keyword_id', 'keyword', 'weaknesses', 'Weaknesses']]
        # list_of_tables = [['course_type_id', 'course_type', 'course_interest', 'Course_Interests']]
        # strengths_weaknesses = [['keyword_id', 'keyword', 'strengths', 'Strengths'],
        #                         ['keyword_id', 'keyword', 'weaknesses', 'Weaknesses']]
        # for each in list_of_tables:
        #     id_df = self.identifier_df(each[0], each[1], each[2], df, each[3])
        #     self.df_to_sql(id_df, each[3])
        #     self.apply_all(each[0], each[1], each[2], df, each[3])
        # print(df)
        # for each in strengths_weaknesses:
        #     idsw_df = self.identifier_list_tables(each[0], each[1], each[2], df, each[3])
        #     self.df_to_sql(idsw_df, each[3])
        #     #self.apply_all(each[0], each[1], each[2], df, each[3])
        courses_df = self.identifier_df('course_id', 'course_name', 'course_name', course_df, 'Courses')
        self.df_to_sql(courses_df, 'Courses')


testing = IdentifierDF()
