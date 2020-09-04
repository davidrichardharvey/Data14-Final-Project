# Imports the class to create the structure for the database. Can run the class by specifying 'to_create' = True upon
# instantiation, or by running the .run_methods()
from s3_project.classes.create_database import ProjectDatabase
from s3_project.classes.joining_class import JoinCleanData


new = ProjectDatabase(to_create=False)  # Change value to true to create database
# merged_dfs = JoinCleanData()

import pandas as pd
print(pd.read_pickle("./merged_dataframe.pkl").columns)

# candidates_dummy = [{'candidate_id': 1, 'first_name': 'Juxhen', 'last_name': 'Bica', 'gender': 'M', 'uni_id': 12,
#                     'degree_id': 1, 'invited_by': int(float('5.0')), 'self_dev': 1, 'geo_flex': 1, 'self_finance': 1, 'result': 1,
#                     'course_interest_id': 1}, {'candidate_id': 2, 'first_name': 'Jade', 'last_name': 'Arthurs',
#                     'gender': 'F', 'uni_id': 8, 'degree_id': 1, 'invited_by': 7, 'self_dev': 1, 'geo_flex': 1,
#                     'self_finance': 1, 'result': 1, 'course_interest_id': 1}, {'candidate_id': 1,
#                     'first_name': 'Mints', 'last_name': 'Shoe', 'gender': 'M', 'uni_id': 19, 'degree_id': 1,
#                     'invited_by': 9, 'self_dev': 1, 'geo_flex': 1, 'self_finance': 1, 'result': 1,
#                     'course_interest_id': 1}]
#
# df = pd.DataFrame(candidates_dummy)

test = JoinCleanData()

df = test.merged_df
test.staff_roles_load()
test.staff_table_load(df)
print(test.assign_fk_staff(df))
#
# # print(test.merged_df.loc[test.merged_df['first_name']=='Brien'])
# # test.candidates_load(df)
# #
# # print(test.merged_df.loc[test.merged_df['last_name']=='Brien'])
pd.set_option('display.max_rows', None)
print(test.merged_df['uni_id'])
test.candidates_load(df)
