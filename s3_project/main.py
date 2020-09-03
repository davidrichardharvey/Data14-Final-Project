#
# from s3_project.classes.cleaning_txt import talent_txt
# from s3_project.classes.academy_class import academy_dataframe
# from s3_project.classes.talent_csv_cleaning import monthly_talent_info
# from s3_project.classes.applicant_info_class import talent_applicant_info
# #
# #
# print(f"Applicant Info Data Frame: {talent_applicant_info.df_talent_json}")
# print(f"Talent Text Files Data Frame: {talent_txt.df}")
# print(f"Academy Data Frame: {academy_dataframe.cleaned_df}")
# print(f"Monthly Talent Data Frame: {monthly_talent_info.df_talent_csv}")


from s3_project.classes.create_database import new
new.create_table_no_keys()
from s3_project.classes.joining_class import merged_dfs

print(merged_dfs.merged_df)


import pandas as pd

print(pd.read_pickle("./merged_dataframe.pkl"))
