import ast
import pyodbc
from s3_project.Config.config_manager import find_variable, find_hidden_variable
from s3_project.functions import all_merges
from s3_project.classes.academy_class import Academy
from s3_project.classes.talent_csv_cleaning import TalentCsv
from s3_project.classes.cleaning_txt import TextFiles
from s3_project.classes.applicant_info_class import ApplicantInfoClean
from s3_project.classes.create_database import ProjectDatabase


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
        self.__sparta.commit()

    def candidates_load(self, df):
        table = 'Candidates'
        table_schema = ast.literal_eval(find_variable(table, 'TABLE SCHEMAS'))
        table_fields = list(table_schema.keys())
        table_fields.pop(0)
        col_join = ', '.join(table_fields)
        columns = f"({col_join})"
        candidates = df[['first_name', 'last_name', 'gender', 'uni_id', 'degree_id', 'invited_by',
                         'self_development', 'geo_flex', 'financial_support_self', 'result']]
        candidates = candidates.rename(columns={'financial_support_self': 'self_finance', 'self_development': 'self_dev'})
        unique_df = candidates.drop_duplicates(keep='first', inplace=False, ignore_index=True)
        values = ''
        for i in range(len(unique_df)):
            tup = f"('{unique_df.loc[i, 'first_name']}', '{unique_df.loc[i, 'last_name']}', '{unique_df.loc[i, 'gender']}', "\
                  f"'{unique_df.loc[i, 'uni_id']}', '{unique_df.loc[i, 'degree_id']}', '{unique_df.loc[i, 'invited_by']}', "\
                  f"'{unique_df.loc[i, 'self_development']}', '{unique_df.loc[i, 'geo_flex']}', " \
                  f"'{unique_df.loc[i, 'financial_support_self']}', '{unique_df.loc[i, 'result']}')"
            values += tup
            values += ', '
        values = values.replace(values[-1], '')
        values = values[:-1]
        query = f"INSERT INTO {table} {columns} VALUES {values}"
        self._sql_query(query)
        query = f"SELECT * FROM {table}"
        return self._sql_query(query)
