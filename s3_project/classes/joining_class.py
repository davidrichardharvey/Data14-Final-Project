import pandas as pd
import numpy as np
#from s3_project.classes.cleaning_txt import talent_txt
#from s3_project.classes.academy_class import academy_dataframe
#from s3_project.classes.talent_csv_cleaning import monthly_talent_info
#from s3_project.classes.applicant_info_class import talent_applicant_info

from s3_project.classes.create_database import ProjectDatabase
from s3_project.Config.config_manager import find_variable
from s3_project.Config.config_manager import find_hidden_variable
import ast


class JoinCleanData(ProjectDatabase):
    def __init__(self):
        super().__init__()
        #self.talent_txt_df = talent_txt.df
        #self.monthly_talent_df = monthly_talent_info.df_talent_csv
        #self.academy_df = academy_dataframe.cleaned_df
        #self.talent_application_df = talent_applicant_info.df_talent_json
        self.staff_roles_dict = {'trainer': 1, 'talent_team': 2}  # should go in config??

    # def first_join(self):
    #     merged_df = pd.merge(self.monthly_talent_df, self.talent_application_df, how='outer', left_on=["first_name",
    #             "last_name", 'invited_date'], right_on=['first_name', 'last_name', 'date'])
    #
    #     return merged_df
    #
    # def reassign_fk_column(self, column_name, df):
    #     # Takes in a df and column_name to reassign foreign key values, returns two data frames which are linked by
    #     # keys
    #     df_notnull = df[df[column_name].notna()]
    #     unique_values = pd.unique(df_notnull[column_name])
    #     primary_key_table = pd.unique(df[column_name])
    #     #print(type(unique_values))
    #     unique_values = pd.Series(np.arange(1,len(unique_values)+1),unique_values)
    #     unique_values = unique_values.to_dict()
    #     unique_values[np.nan] = np.nan
    #     #print(unique_values)
    #     df[column_name] = df[column_name].map(unique_values.get)
    #     return df, pd.DataFrame(primary_key_table, columns=[column_name])

    # def _sql_query(self, sql_query):
    #     return new.cursor.execute(sql_query)

    def staff_roles_load(self):
        table = 'Staff_Roles'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = tuple(table_schema.keys())
        entries = ''
        for role in self.staff_roles_dict:
            tup = f"({role})"
            entries += tup
            while role != list(self.staff_roles_dict.keys())[-1]:
                entries += ', '
        print(entries)
        query = f"""
                INSERT INTO {table} {table_fields}
                VALUES {entries}; 
                """
        self._sql_query(query)
        query = f"SELECT * FROM {table};"
        return self._sql_query(query)

    def staff_table_load(self, df):
        table = 'Staff'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = list(table_schema.keys())
        table_fields.pop(0)
        print(table_fields)
        col_join = ', '.join(table_fields)
        print(col_join)
        columns = f"({col_join})"
        print(columns)

        trainers = df[['trainer_first_name', 'trainer_last_name']]
        trainers_filt = trainers[trainers.notna()]
        trainers_filt['role_id'] = self.staff_roles_dict['trainer']
        trainers_filt.rename({'trainer_first_name': 'first_name', 'trainer_last_name': 'last_name'}, axis=1, inplace=True)
        talent = df[['inv_by_firstname', 'inv_by_lastname']]
        talent_filt = talent[talent.notna()]
        talent_filt['role_id'] = self.staff_roles_dict['talent_team']
        talent_filt.rename({'inv_by_firstname': 'first_name', 'inv_by_lastname': 'last_name'}, axis=1, inplace=True)
        df_joined = pd.concat([trainers_filt, talent_filt])
        unique_df = df_joined.drop_duplicates(keep='first', inplace=False, ignore_index=True)
        print(unique_df)

        values = ''
        for i in range(len(unique_df)):
            #tup = (unique_df.loc[i, 'first_name'], unique_df.loc[i, 'last_name'])
            tup = f"('{unique_df.loc[i, 'first_name']}', '{unique_df.loc[i, 'last_name']}', {unique_df.loc[i, 'role_id']})"
            values += tup
            values += ', '
        #values = values.replace(values[-1], '')
        values = values[:-2]
        print(values)
        query = f"INSERT INTO {table} {columns} VALUES {values};"
        self._sql_query(query)
        query = f"SELECT * FROM {table};"
        return self._sql_query(query)

    # def assign_fk_staff(self, df):
    #     table = 'Staff'
    #     list_entries = []
    #     fk_dict_trainers = {}
    #     fk_dict_talent = {}
    #     for key in self.staff_roles_dict:
    #         role_id = self.staff_roles_dict[key]
    #         query = f"SELECT staff_id, first_name, last_name FROM {table} WHERE role_id = {role_id}"
    #         list_entries.append(list(self._sql_query(query)))
    #     for entry in list_entries[0]:
    #         fk_dict_trainers[entry[1] + ' ' + entry[2]] = entry[0]
    #     for entry in list_entries[1]:
    #         fk_dict_talent[entry[1] + ' ' + entry[2]] = entry[0]
    #
    #     df['trainer_id'] = np.nan(len(df))
    #     df['talent_id'] = np.nan(len(df))
    #     for i in range(len(df)):
    #         trainer_id = fk_dict_trainers[df.loc[i, 'trainer_first_name'] + ' ' + df.loc[i, 'trainer_last_name']]
    #         df.loc[i, 'trainer_id'] = trainer_id
    #         talent_id = fk_dict_trainers[df.loc[i, 'trainer_first_name'] + ' ' + df.loc[i, 'trainer_last_name']]
    #         df.loc[i, 'talent_id'] = talent_id


#clean_data = JoinCleanData()
