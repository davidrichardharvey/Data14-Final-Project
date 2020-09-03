# Imports the class to create the structure for the database. Can run the class by specifying 'to_create' = True upon
# instantiation, or by running the .run_methods()
from s3_project.classes.create_database import ProjectDatabase
from s3_project.classes.joining_class import JoinCleanData


# new = ProjectDatabase(to_create=False)  # Change value to true to create database
# merged_dfs = JoinCleanData()

# import pandas as pd
# print(pd.read_pickle("./merged_dataframe.pkl").columns)

new = ProjectDatabase(to_create=True)  # Change value to true to create database
merged_dfs = JoinCleanData()
staff_table = (merged_dfs.creating_table_df('Staff'))
trainers = staff_table[staff_table['role_id'] == '1']
print(staff_table)
# merged_dfs.create_tools_slice(merged_dfs.creating_table_df('Tools'))

