# Imports the class to create the structure for the database. Can run the class by specifying 'to_create' = True upon
# instantiation, or by running the .run_methods()
from s3_project.classes.create_database import ProjectDatabase
from s3_project.classes.joining_class import JoinCleanData

new = ProjectDatabase(to_create=False)  # Change value to true to create database

merged_dfs = JoinCleanData()


# merged_dfs.create_tools_slice(merged_dfs.creating_table_df('Tools'))


