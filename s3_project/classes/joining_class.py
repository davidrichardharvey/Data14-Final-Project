import pandas as pd
import numpy as np
from s3_project.Config.config_manager import find_variable
from s3_project.classes.cleaning_txt import talent_txt
from s3_project.classes.academy_class import academy_dataframe
from s3_project.classes.create_database import new
from s3_project.classes.talent_csv_cleaning import monthly_talent_info
from s3_project.classes.applicant_info_class import talent_applicant_info
import ast


class JoinCleanData:
    def __init__(self):
        self.talent_txt_df = talent_txt.df
        self.monthly_talent_df = monthly_talent_info.df_talent_csv
        self.academy_df = academy_dataframe.cleaned_df
        self.talent_application_df = talent_applicant_info.df_talent_json

    def first_join(self):
        merged_df1 = pd.merge(self.monthly_talent_df, self.talent_application_df, how='outer', left_on=["first_name",
                                                                                                        "last_name",
                                                                                                        'invited_date'],
                              right_on=['first_name', 'last_name', 'date'])
        # merged_df2 = pd.merge(merged_df1, self.talent_txt_df, how='outer', left_on=["first_name",
        #         "last_name", 'invited_date'], right_on=['first_name', 'last_name', 'date'])
        return merged_df1

    def reassign_fk_column(self, column_name, df):
        # Takes in a df and column_name to reassign foreign key values, returns two data frames which are linked by
        # keys
        df_notnull = df[df[column_name].notna()]
        unique_values = pd.unique(df_notnull[column_name])
        primary_key_table = pd.unique(df[column_name])
        # print(type(unique_values))
        unique_values = pd.Series(np.arange(1, len(unique_values) + 1), unique_values)
        unique_values = unique_values.to_dict()
        unique_values[np.nan] = np.nan
        # print(unique_values)
        df[column_name] = df[column_name].map(unique_values.get)
        return df, pd.DataFrame(primary_key_table, columns=[column_name])

    def _sql_query(self, sql_query):
        return new.cursor.execute(sql_query)

    def candidates_load(self, df):
        table = 'Candidates'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = list(table_schema.keys())
        table_fields.pop(0)
        col_join = ', '.join(table_fields)
        columns = f"({col_join})"
        candidates = df[['first_name', 'last_name', 'gender', 'uni_id', 'degree_id', 'invited_by',
                         'self_dev', 'geo_flex', 'self_finance', 'result']]
        unique_df = candidates.drop_duplicates(keep='first', inplace=False, ignore_index=True)
        values = ''
        for i in range(len(unique_df)):
            tup = f"('{unique_df.loc[i, 'first_name']}', '{unique_df.loc[i, 'last_name']}', '{unique_df.loc[i, 'gender']}', "\
                  f"'{unique_df.loc[i, 'uni_id']}', '{unique_df.loc[i, 'degree_id']}', '{unique_df.loc[i, 'invited_by']}', "\
                  f"'{unique_df.loc[i, 'self_dev']}', '{unique_df.loc[i, 'geo_flex']}', " \
                  f"'{unique_df.loc[i, 'self_finance']}', '{unique_df.loc[i, 'result']}')"
            values += tup
            values += ', '
        values = values.replace(values[-1], '')
        values = values[:-1]
        query = f"INSERT INTO {table} {columns} VALUES {values}"
        self._sql_query(query)
        query = f"SELECT * FROM {table}"
        return self._sql_query(query)


clean_data = JoinCleanData()

# 4.	For each row in the table, check to see whether or not they are already in the candidates table
# a.	For this to be the case, the following must match:
# i.	First Name
# ii.	Last Name
# iii.	Gender
# iv.	Uni id
# v.	Degree id
# b.	If they are not already in the candidate table, add them to it (thus giving them a new candidate ID)
# c.	Create a new column in the dataframe which stores the candidate’s ID for each row
