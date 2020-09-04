# from s3_project.functions import all_merges
# from s3_project.classes.academy_class import Academy
# from s3_project.classes.talent_csv_cleaning import TalentCsv
# from s3_project.classes.cleaning_txt import TextFiles
# from s3_project.classes.applicant_info_class import ApplicantInfoClean
from s3_project.Config.config_manager import find_hidden_variable, find_variable
import pandas as pd
import urllib
import ast
import pyodbc
import numpy as np
from sqlalchemy import create_engine

# academy_dataframe = Academy()
# monthly_talent_info = TalentCsv()
# talent_txt = TextFiles()
# talent_applicant_info = ApplicantInfoClean()


class JoinCleanData:
    def __init__(self):
        # self.sparta_day_txt = talent_txt.df
        # self.monthly_applicant_csv = monthly_talent_info.df_talent_csv
        # self.academy_scores_csv = academy_dataframe.cleaned_df
        # self.applicant_info_json = talent_applicant_info.df_talent_json
        # self.merged_df = all_merges(self.monthly_applicant_csv, self.sparta_day_txt, self.applicant_info_json,
        #                             self.academy_scores_csv)
        self.merged_df = pd.read_pickle("./merged_dataframe.pkl")
        # self.Cities = self.merged_df[['city']]
        # self.Course_Interests = self.merged_df[['course_interest']]
        # self.Courses = self.merged_df[['course_name', 'course_start_date', 'course_length']]
        # self.Degrees = self.merged_df[['degree']]
        # self.Locations = self.merged_df[['location']]
        # self.Staff_Roles = pd.DataFrame({'role': ['Trainer', 'Talent']})
        # self.Strengths = self.merged_df[['strengths']]
        # self.Universities = self.merged_df[['uni']]
        # self.Weaknesses = self.merged_df[['weaknesses']]

        # Establishing connection to server
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

        # self.params = urllib.parse.quote_plus(self.connection_string)
        # self.engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % self.params)
        # self.input_tables_to_sql()
        # self.apply_reassign()

    def _sql_query(self, sql_query):
        return self.cursor.execute(sql_query)

    def df_to_sql(self, df, sql_table):
        # This method writes the df to the SQL database
        df.to_sql(sql_table, con=self.engine, index=False, if_exists='append', chunksize=1000)

    def get_id(self, sql_id, sql_column_name, table):
        # This method gets the ID's from the database for later use
        fk_key_dict = {}
        query = f"SELECT {sql_id}, {sql_column_name} FROM {table};"
        for index, value in self._sql_query(query):
            fk_key_dict[value] = index
        return fk_key_dict

    def values_from_list(self, column_name, df):
        # This method returns unique items from a column which only contains lists
        df_notnull = df[df[column_name].notna()]
        list_append = []
        for each in df_notnull[column_name]:
            for item in each:
                if item not in list_append:
                    list_append.append(item)
        return list_append

    def identifier_list_tables(self, sql_id, sql_column_name, df_column_name, df, table):
        # This method returns a identifier table for columns that have lists and ensures they are unique in the database
        unique_values = self.values_from_list(df_column_name, df)
        column_name_dict = self.get_id(sql_id, sql_column_name, table)
        unique_values = pd.Series(unique_values)
        for index, each in unique_values.iteritems():
            if each in column_name_dict.keys():
                unique_values = unique_values.drop(index=index)
        id_df = pd.DataFrame(unique_values, columns=[sql_column_name])
        return id_df

    def identifier_df(self, sql_id, sql_column_name, df_column_name, df, table):
        # This method creates a data frame for a column and ensures they are only unique values
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

    def input_tables_to_sql(self):
        # This loads all the data to SQL
        id_tables = ['Locations', 'Universities', 'Degrees', 'Course_Interests', 'Cities', 'Courses', 'Staff_Roles',
                     'Strengths', 'Weaknesses']
        df_list = [self.Locations, self.Universities, self.Degrees, self.Course_Interests, self.Cities, self.Courses,
                   self.Staff_Roles, self.Strengths, self.Weaknesses]
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
                self.sparta.commit()
            else:
                id_df = self.identifier_df(sql_id, sql_column, df_column, df, id_tables[i])
                print(f"Loading {id_tables[i]} table into database")
                self.df_to_sql(id_df, id_tables[i])
                self.sparta.commit()
        print('9 tables have successfully loaded')

    def reassign_values(self, sql_id, sql_column, df_column, df, table):
        # This method reads the keys from the database and maps onto a column
        id_dict = self.get_id(sql_id, sql_column, table)
        df[df_column] = df[df_column].map(id_dict)
        df = df.rename(columns={df_column: sql_id})
        return df

    def reassign_weaknesses(self, df_column):
        # This methods reassigns every element in the weaknesses column to foreign keys
        id_dict = self.get_id('keyword_id', 'keyword', 'Weaknesses')
        list_of_keywords = []
        if type(df_column) is not float:
            for item in df_column:
                value = id_dict.get(item)
                list_of_keywords.append(value)
        return list_of_keywords

    def reassign_strengths(self, df_column):
        # This methods reassigns every element in the strengths column to foreign keys
        id_dict = self.get_id('keyword_id', 'keyword', 'Strengths')
        list_of_keywords = []
        if type(df_column) is not float:
            for item in df_column:
                value = id_dict.get(item)
                list_of_keywords.append(value)
        return list_of_keywords

    def apply_reassign(self):
        # This method reads the keys from the database and assigns the foreign key value to the appropriate columns
        print('Reassigning values to location column')
        self.merged_df = self.reassign_values('location_id', 'location', 'location', self.merged_df, 'Locations')

        print('Reassigning values to city column')
        self.merged_df = self.reassign_values('city_id', 'city', 'city', self.merged_df, 'Cities')

        print('Reassigning values to course interest column')
        self.merged_df = self.reassign_values('course_type_id', 'course_type', 'course_interest', self.merged_df,
                                              'Course_Interests')

        print('Reassigning values to courses column')
        self.merged_df = self.reassign_values('course_id', 'course_name', 'course_name', self.merged_df, 'Courses')

        print('Reassigning values to degree column')
        self.merged_df = self.reassign_values('degree_id', 'degree', 'degree', self.merged_df, 'Degrees')

        print('Reassigning values to uni column')
        self.merged_df = self.reassign_values('uni_id', 'uni', 'uni', self.merged_df, 'Universities')

        print('Reassigning values to strengths column')
        self.merged_df['strengths'] = self.merged_df['strengths'].apply(self.reassign_strengths)

        print('Reassigning values to weaknesses column')
        self.merged_df['weaknesses'] = self.merged_df['weaknesses'].apply(self.reassign_weaknesses)

        print('Reassignment completed')





    def creating_table_df(self, table_name):
        # Creates a data frame with all of the existing data for that table in the database
        sql_table = list(self._sql_query(f"SELECT * FROM {table_name}"))
        sql_table_list = []
        for row in sql_table:
            sql_table_list.append(list(row))

        # Gets the column names for the data frame
        columns = []
        for column_name in ast.literal_eval(find_variable(table_name, 'TABLE SCHEMAS')):
            columns.append(column_name)

        # Creates the data frame corresponding to the data in the database
        if len(sql_table_list) > 0:
            table_array = np.array(sql_table_list).reshape(len(sql_table_list), len(sql_table_list[0]))
            table_df = pd.DataFrame(table_array)
            for index in range(0, len(columns)):
                table_df.rename(columns={index: columns[index]}, inplace=True)
            return table_df
        else:
            table_df = pd.DataFrame(columns=columns)
            return table_df

    def create_tools_slice(self):
        # Returns a table for all the information in the data frame corresponding to the tools scores
        new_info = []
        distinct_tools = []
        candidates_df = self.creating_table_df('Candidates')
        self.merged_df['candidate_id'] = range(1, 4717)  # Will need to remove and find a way to deal with this. Can't do it yet though because dev is only up to step 2

        # Getting a list of all of the tools
        for row in self.merged_df['tech_self_score']:
            if type(row) == dict:
                for tool in row:
                    if tool not in distinct_tools:
                        distinct_tools.append(tool)

        # Creating a data frame with all of the scores for the different tools for each candidate
        rows_updated = 0
        df_exists = False
        for row in self.merged_df['candidate_id']:
            print(f'Rows Updated: {rows_updated}')
            for tool in distinct_tools:
                try:
                    score = self.merged_df['tech_self_score'].to_dict()[row][tool]
                    new_info.append({'candidate_id': row, 'tool': tool, 'score': score})
                    df_exists = True
                except TypeError:
                    score = np.nan
                except KeyError:
                    score = np.nan
        if df_exists:
            new_df = pd.DataFrame(new_info)
            new_df = new_df[~pd.isna(new_df['score'])]
            new_df['id_t_s'] = new_df['candidate_id'].map(str) + new_df['tool'] + new_df['score'].map(str)
            table_df = self.creating_table_df('Tools')
            table_df['id_t_s'] = table_df['candidate_id'].map(str) + table_df['tool'] + table_df['score'].map(str)
            new_df = new_df[~new_df['id_t_s'].isin(table_df['id_t_s'])]
            new_df.drop('id_t_s', inplace=True, axis=1)
            return [True, new_df]
        else:
            return [False]

    def create_slice(self, table_df, auto_inc_col=None, not_null_columns=()):
        # Creates a new data frame by slicing the large data frame and dropping rows already in the database
        new_info = []
        if auto_inc_col:
            self.merged_df[auto_inc_col] = np.nan  # Creates a column of NaN values for the auto incrementing PK

        # Creates a slice of the data frame
        for column in table_df.columns:
            new_column_info = self.merged_df[column]
            new_info.append(new_column_info)
        new_info_df = pd.concat(new_info, axis=1)

        # Filters out the rows that already exist in the data
        for column in table_df.columns:
            if column != auto_inc_col:
                new_info_df = new_info_df[~new_info_df[column].isin(table_df[column])]

        # Filters out the rows that contain null values in non-nullable columns
        for column in not_null_columns:
            new_info_df = new_info_df[~pd.isna(new_info_df[column])]

        new_df = pd.concat([table_df, new_info_df]).drop_duplicates().reset_index(drop=True)
        return new_df
