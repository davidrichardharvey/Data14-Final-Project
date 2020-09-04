from s3_project.functions import all_merges
from s3_project.classes.academy_class import Academy
from s3_project.classes.talent_csv_cleaning import TalentCsv
from s3_project.classes.cleaning_txt import TextFiles
from s3_project.classes.applicant_info_class import ApplicantInfoClean
from s3_project.Config.config_manager import find_hidden_variable, find_variable

import pandas as pd
import urllib
import ast
import pyodbc
import numpy as np
from sqlalchemy import create_engine


academy_dataframe = Academy()
monthly_talent_info = TalentCsv()
talent_txt = TextFiles()
talent_applicant_info = ApplicantInfoClean()


class JoinCleanData:
    def __init__(self):
        self.sparta_day_txt = talent_txt.df
        self.monthly_applicant_csv = monthly_talent_info.df_talent_csv
        self.academy_scores_csv = academy_dataframe.cleaned_df
        self.applicant_info_json = talent_applicant_info.df_talent_json
        self.merged_df = all_merges(self.monthly_applicant_csv, self.sparta_day_txt, self.applicant_info_json,
                                    self.academy_scores_csv)

        self.merged_df = pd.read_pickle('merged_dataframe.pkl')
        self.staff_roles_dict = {'Trainer': 1, 'Talent': 2}
        self.Cities = self.merged_df[['city']]
        self.Course_Interests = self.merged_df[['course_interest']]
        self.Courses = self.merged_df[['course_name', 'course_start_date', 'course_length']]
        self.Degrees = self.merged_df[['degree']]
        self.Locations = self.merged_df[['location']]
        self.Staff_Roles = pd.DataFrame({'role': ['Trainer', 'Talent']})
        self.Strengths = self.merged_df[['strengths']]
        self.Universities = self.merged_df[['uni']]
        self.Weaknesses = self.merged_df[['weaknesses']]
        #

        # Establishing connection to server
        self.__server = find_hidden_variable('server')
        self.__database = find_hidden_variable('database')
        self.__username = find_hidden_variable('username')
        self.__password = find_hidden_variable('password')
        self.__connection_string = "DRIVER={SQL Server};"
        self.__connection_string += f"SERVER={self.__server};"
        self.__connection_string += f"DATABASE={self.__database};"
        self.__connection_string += f"UID={self.__username};"
        self.__connection_string += f"PWD={self.__password}"
        self.__sparta = pyodbc.connect(self.__connection_string)
        self.__cursor = self.__sparta.cursor()

        self.__params = urllib.parse.quote_plus(self.__connection_string)
        self.__engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % self.__params)
        self.input_tables_to_sql()
        self.apply_reassign()
        self.staff_roles_load()
        self.staff_table_load()
        self.assign_fk_staff()
        # self.candidates_load()
        self.assign_fk_candidates()
        self.create_tools_slice()

    def _sql_id_query(self, sql_query):
        return self.__cursor.execute(sql_query)

    def _sql_query(self, sql_query):
        self.__cursor.execute(sql_query)
        self.__sparta.commit()

    def df_to_sql(self, df, sql_table):
        # This method writes the df to the SQL database
        df.to_sql(sql_table, con=self.__engine, index=False, if_exists='append', chunksize=1000)

    def get_id(self, sql_id, sql_column_name, table):
        # This method gets the ID's from the database for later use
        fk_key_dict = {}
        query = f"SELECT {sql_id}, {sql_column_name} FROM {table};"
        for index, value in self._sql_id_query(query):
            fk_key_dict[value] = int(float(index))
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
            column_map_dict[df_keys[i]] = column_keys[i + 1]
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
                self.__sparta.commit()
            else:
                id_df = self.identifier_df(sql_id, sql_column, df_column, df, id_tables[i])
                print(f"Loading {id_tables[i]} table into database")
                self.df_to_sql(id_df, id_tables[i])
                self.__sparta.commit()
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

        # print('Reassigning values to strengths column')
        # self.merged_df['strengths'] = self.merged_df['strengths'].apply(self.reassign_strengths)
        #
        # print('Reassigning values to weaknesses column')
        # self.merged_df['weaknesses'] = self.merged_df['weaknesses'].apply(self.reassign_weaknesses)
        #
        # print('Reassignment completed')

    def staff_roles_load(self):
        table = 'Staff_Roles'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = list(table_schema.keys())
        table_fields.pop(0)
        col = table_fields[0].strip("'")
        column = f"({col})"
        values = ''
        for role in self.staff_roles_dict:
            tup = f"('{role}')"
            values += tup
            values += ', '
        values = values[:-2]
        query = f"""
                INSERT INTO {table} {column}
                VALUES {values};
                """
        self._sql_query(query)
        query = f"SELECT * FROM {table};"
        return self._sql_query(query)

    def staff_table_load(self):
        df = self.merged_df
        table = 'Staff'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = list(table_schema.keys())
        table_fields.pop(0)
        col_join = ', '.join(table_fields)
        columns = f"({col_join})"
        trainers = df[['trainer_first_name', 'trainer_last_name']]
        trainers['role_id'] = self.staff_roles_dict['Trainer']
        trainers.rename({'trainer_first_name': 'first_name', 'trainer_last_name': 'last_name'}, axis=1, inplace=True)
        talent = df[['inv_by_firstname', 'inv_by_lastname']]
        talent['role_id'] = self.staff_roles_dict['Talent']
        talent.rename({'inv_by_firstname': 'first_name', 'inv_by_lastname': 'last_name'}, axis=1, inplace=True)
        df_joined = pd.concat([trainers, talent])
        df_joined = df_joined.dropna()
        unique_df = df_joined.drop_duplicates(keep='first', inplace=False, ignore_index=True)
        values = ''
        for i in range(len(unique_df)):
            tup = f"('{unique_df.loc[i, 'first_name']}', '{unique_df.loc[i, 'last_name']}', {unique_df.loc[i, 'role_id']})"
            values += tup
            values += ', '
        values = values[:-2]
        query = f"INSERT INTO {table} {columns} VALUES {values};"
        self._sql_query(query)
        query = f"SELECT * FROM {table};"
        return self._sql_query(query)

    def assign_fk_staff(self):
        df = self.merged_df
        table = 'Staff'
        list_entries = []
        fk_dict_trainers = {}
        fk_dict_talent = {}
        my_dict = self.staff_roles_dict
        for key, value in my_dict.items():
            role_id = value
            query = f"SELECT staff_id, first_name, last_name FROM Staff WHERE role_id = {role_id};"
            records = self.__cursor.execute(query)
            all_values = records.fetchall()
            list_entries.append(all_values)

        for entry in list_entries[0]:
            fk_dict_trainers[entry[1] + ' ' + entry[2]] = int(float(entry[0]))
        for entry in list_entries[1]:
            fk_dict_talent[entry[1] + ' ' + entry[2]] = int(float(entry[0]))

        df['trainers_id'] = df['trainer_first_name'].map(str) + ' ' + df['trainer_last_name'].map(str)
        df['trainers_id'] = df['trainers_id'].map(fk_dict_trainers)
        df['talent_id'] = df['inv_by_firstname'].map(str) + ' ' + df['inv_by_lastname'].map(str)
        df['talent_id'] = df['talent_id'].map(fk_dict_talent)
        return df[['trainers_id', 'talent_id']]

    def candidates_load(self):
        print('Loading Candidates table into database')
        df = self.merged_df
        table = 'Candidates'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = list(table_schema.keys())
        table_fields.pop(0)
        col_join = ', '.join(table_fields)
        columns = f"({col_join})"
        candidates = df[['first_name', 'last_name', 'gender', 'uni_id', 'degree_id', 'talent_id',
                         'self_development', 'geo_flex', 'financial_support_self', 'result', 'course_type_id']]
        candidates = candidates.fillna(1)
        candidates['uni_id'] = candidates['uni_id'].apply(lambda x: int(float(x)))
        candidates['degree_id'] = candidates['degree_id'].apply(lambda x: int(float(x)))
        candidates['talent_id'] = candidates['talent_id'].apply(lambda x: int(float(x)))
        candidates['course_type_id'] = candidates['course_type_id'].apply(lambda x: int(float(x)))
        unique_df = candidates.drop_duplicates(keep='first', inplace=False, ignore_index=True)
        unique_df = unique_df.rename(columns={'course_type_id': 'course_interest_id', 'self_development': 'self_dev',
                                              'financial_support_self': 'self_finance', 'invited_by': 'talent_id'})
        unique_df['last_name'] = unique_df['last_name'].map(lambda x: x.replace("'", ' '))
        unique_df['first_name'] = unique_df['first_name'].map(lambda x: x.replace("'", ' '))
        for i in range(len(unique_df)):
            values = ''
            tup = f"('{unique_df.loc[i, 'first_name']}', '{unique_df.loc[i, 'last_name']}', '{unique_df.loc[i, 'gender']}', " \
                  f"'{unique_df.loc[i, 'uni_id']}', '{unique_df.loc[i, 'degree_id']}', '{unique_df.loc[i, 'talent_id']}', " \
                  f"'{unique_df.loc[i, 'self_dev']}', '{unique_df.loc[i, 'geo_flex']}', " \
                  f"'{unique_df.loc[i, 'self_finance']}', '{unique_df.loc[i, 'result']}', " \
                  f"'{unique_df.loc[i, 'course_interest_id']}')"
            values += tup
            query = f"INSERT INTO {table} {columns} VALUES {values}"
            self._sql_query(query)
        print('Candidates table loaded in database')

    def assign_fk_candidates(self):
        df = self.merged_df
        table = 'Candidates'
        fk_dict_candidates = {}
        query = f"SELECT CONCAT(first_name, ' ', last_name), candidate_id FROM {table};"
        records = self.__cursor.execute(query)
        all_values = records.fetchall()
        for candidate in all_values:
            fk_dict_candidates[candidate[0]] = candidate[1]
        df['candidate_id'] = df['first_name'] + ' ' + df['last_name']
        df['candidate_id'] = df['candidate_id'].map(fk_dict_candidates)
        self.merged_df = df
        self.merged_df.set_index('candidate_id', inplace=True)

    # Charlie's Code
    def creating_table_df(self, table_name):
        # Creates a data frame with all of the existing data for that table in the database

        print(self.merged_df)
        sql_table = list(self._sql_id_query(f"SELECT * FROM {table_name}"))
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

        # Getting a list of all of the tools
        for row in self.merged_df['tech_self_score']:
            if type(row) == dict:
                for tool in row:
                    if tool not in distinct_tools:
                        distinct_tools.append(tool)

        # Creating a data frame with all of the scores for the different tools for each candidate
        rows_updated = 0
        df_exists = False
        for row in self.merged_df.index:
            if rows_updated % 100 == 0:
                print(f'Rows Updated: {rows_updated}')
            for tool in distinct_tools:
                try:
                    score = self.merged_df['tech_self_score'].to_dict()[int(row)][tool]
                    new_info.append({'candidate_id': row, 'tool': tool, 'score': score})
                    df_exists = True
                except TypeError:
                    score = np.nan
                except KeyError:
                    score = np.nan
                except ValueError:
                    score = np.nan
            rows_updated += 1
        if df_exists:
            new_df = pd.DataFrame(new_info)
            new_df = new_df[~pd.isna(new_df['score'])]
            new_df['id_t_s'] = new_df['candidate_id'].map(str).map(lambda x: x.replace('.0', '')) + \
                               new_df['tool'] + new_df['score'].map(str)
            table_df = self.creating_table_df('Tools')
            table_df['id_t_s'] = table_df['candidate_id'].map(str) + table_df['tool'] + table_df['score'].map(str)
            new_df = new_df[~new_df['id_t_s'].isin(table_df['id_t_s'])]
            new_df.drop('id_t_s', inplace=True, axis=1)
            new_df.to_sql('Tools', con=self.__engine, index=False, if_exists='append', chunksize=rows_updated)
        else:
            return [False]


