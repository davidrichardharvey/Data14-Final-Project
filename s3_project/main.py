# from s3_project.classes.cleaning_txt import talent_txt
#from s3_project.classes.academy_class import academy_dataframe
# from s3_project.classes.talent_csv_cleaning import monthly_talent_info
# from s3_project.classes.applicant_info_class import talent_applicant_info
# from s3_project.classes.create_database import new

# print(f"Applicant Info Data Frame: {talent_applicant_info.df_talent_json}")
# print(f"Talent Text Files Data Frame: {talent_txt.df}")
#print(f"Academy Data Frame: {academy_dataframe.cleaned_df}")
# print(f"Monthly Talent Data Frame: {monthly_talent_info.df_talent_csv}")
#
# new.create_table_no_keys()

from s3_project.classes.identifier_df import testing
#
# #print(list(testing._sql_query('SELECT * FROM INFORMATION_SCHEMA.TABLES')))

# print(testing.talent_txt)
# #print(testing.identifier_df('city', testing.all_data, 'cities'))
#
# #print(testing.get_strengths())
# #print(testing.get_weaknesses())
# # df = testing.all_data
# # df['duplicated'] = df.duplicated()
# # print(df.loc[df['first_name']=='Rafi'])
# #testing.cities_table()
# # SELECT COUNT(*)
# # FROM INFORMATION_SCHEMA.TABLES

import pandas as pd
pd.set_option('display.max_columns', None)
df = testing.df
print(df)
#print(testing.identifier_list_tables('keyword_id', 'keyword', 'strengths', df, 'Strengths'))
#print(testing.identifier_list_tables('keyword_id', 'keyword', 'weaknesses', df, 'Weaknesses'))
# df = testing.df
# id_df = testing.identifier_df('degree', df, 'Degrees')
#print(testing.identifier_df('city_id', 'city', 'city', df, 'Cities'))
# print(testing.identifier_df_to_sql('uni', df, 'Universities'))
testing.input_sql_tables()
#testing.apply_all()
#print(testing.get_id('city_id', 'city', 'Cities'))
#
# # print(testing.assign_city())
# # testing.df_to_sql(testing.all_data, 'talent_csv')

