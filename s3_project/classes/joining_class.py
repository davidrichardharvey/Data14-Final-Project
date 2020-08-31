from s3_project.classes.cleaning_txt import talent_txt
from s3_project.classes.academy_class import academy_dataframe
from s3_project.classes.talent_csv_cleaning import monthly_talent_info
#from s3_project.classes.applicant_info_class import talent_applicant_info
import pandas as pd
import numpy as np

class JoinCleanData:
    def __init__(self):
        self.talent_txt_df = talent_txt.to_dataframe()
        self.monthly_talent_df = monthly_talent_info.df_talent_csv
        self.academy_df = academy_dataframe.cleaned_df
        self.talent_application_df = ''

    def first_join(self):
        talent_txt_df = talent_txt.to_dataframe()
        monthly_df = monthly_talent_info.df_talent_csv
        merged_df = pd.merge(monthly_df, talent_txt_df, how='outer', left_on=["first_name", "last_name", 'invited_date']
                             , right_on=['first_name', 'last_name', 'date'])
        return merged_df

    def make_table(self, list_of_columns):
        df = self.join_all[list_of_columns]
        return df

    def reassign_FK_column(self, column_name, df):
        # Takes in a df and column_name to reassign foreign key values, returns two data frames which are linked by
        # keys
        df_notnull = df[df[column_name].notna()]
        unique_values = pd.unique(df_notnull[column_name])
        primary_key_table = pd.unique(df[column_name])
        #print(type(unique_values))
        unique_values = pd.Series(np.arange(1,len(unique_values)+1),unique_values)
        unique_values = unique_values.to_dict()
        unique_values[np.nan] = np.nan
        #print(unique_values)
        df[column_name] = df[column_name].map(unique_values.get)
        return df, pd.DataFrame(primary_key_table, columns=['city'])






clean_data = JoinCleanData()
