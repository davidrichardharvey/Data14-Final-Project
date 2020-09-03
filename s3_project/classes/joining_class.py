from s3_project.functions import all_merges
from s3_project.classes.academy_class import Academy
from s3_project.classes.talent_csv_cleaning import TalentCsv
from s3_project.classes.cleaning_txt import TextFiles
from s3_project.classes.applicant_info_class import ApplicantInfoClean

import pandas as pd
import numpy as np
import pyodbc
from s3_project.Config.config_manager import find_variable
from s3_project.Config.config_manager import find_hidden_variable
import ast


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
        self.merged_df = pd.read_pickle('merged_dataframe.pkl')
        self.staff_roles_dict = {'trainer': 1, 'talent_team': 2}  # should go in config??
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


    def _sql_query(self, sql_query):
        self.__cursor.execute(sql_query)
        #self.__sparta.commit()  # remove when needed

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
        print(values)
        query = f"""
                INSERT INTO {table} {column}
                VALUES {values};
                """
        self._sql_query(query)
        query = f"SELECT * FROM {table};"
        return self._sql_query(query)

    def staff_table_load(self, df):
        table = 'Staff'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = list(table_schema.keys())
        table_fields.pop(0)
        col_join = ', '.join(table_fields)
        columns = f"({col_join})"

        trainers = df[['trainer_first_name', 'trainer_last_name']]
        #trainers_filt = trainers[pd.isna(trainers['trainer_first_name'])]
        trainers['role_id'] = self.staff_roles_dict['trainer']
        trainers.rename({'trainer_first_name': 'first_name', 'trainer_last_name': 'last_name'}, axis=1, inplace=True)
        talent = df[['inv_by_firstname', 'inv_by_lastname']]
        #talent_filt = talent[talent.notna()]
        talent['role_id'] = self.staff_roles_dict['talent_team']
        talent.rename({'inv_by_firstname': 'first_name', 'inv_by_lastname': 'last_name'}, axis=1, inplace=True)
        df_joined = pd.concat([trainers, talent])
        df_joined = df_joined[df_joined['first_name'].isin(['nan', 'None'])]
        print(df_joined)
        unique_df = df_joined.drop_duplicates(keep='first', inplace=False, ignore_index=True)
        #print(trainers_filt[pd.isna(trainers_filt['first_name'])])
        values = ''
        for i in range(len(unique_df)):
            tup = f"('{unique_df.loc[i, 'first_name']}', '{unique_df.loc[i, 'last_name']}', {unique_df.loc[i, 'role_id']})"
            values += tup
            values += ', '
        values = values[:-2]
        print(values)
        query = f"INSERT INTO {table} {columns} VALUES {values};"
        self._sql_query(query)
        query = f"SELECT * FROM {table};"
        return self._sql_query(query)

    def assign_fk_staff(self, df):
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
            print(all_values)

            list_entries.append(all_values)
        print(list_entries)

        for entry in list_entries[0]:
            fk_dict_trainers[entry[1] + ' ' + entry[2]] = entry[0]
        for entry in list_entries[1]:
            fk_dict_talent[entry[1] + ' ' + entry[2]] = entry[0]


        # for i in range(len(df)):

        df['trainers_names'] = df['trainer_first_name'].map(str) + ' ' + df['trainer_last_name'].map(str)
        df['trainers_names'] = df['trainers_names'].map(fk_dict_trainers)
        print(df[['trainer_first_name','trainers_names']])
        # df['trainer_id'] = np.zeros(len(df))
        # df['talent_id'] = np.zeros(len(df))
        # print(df.loc[1, 'trainer_first_name'])
        # for i in range(len(df)):
        #     print(df.loc[i, 'trainer_first_name'] + ' ' + df.loc[i, 'trainer_last_name'])
        #     trainer_id = fk_dict_trainers[df.loc[i, 'trainer_first_name'] + ' ' + df.loc[i, 'trainer_last_name']]
        #     df.loc[i, 'trainer_id'] = trainer_id
        #     talent_id = fk_dict_trainers[df.loc[i, 'inv_by_firstname'] + ' ' + df.loc[i, 'inv_by_lastname']]
        #     df.loc[i, 'talent_id'] = talent_id
        # return df[['trainer_id', 'talent_id']]




