# Imports the class to create the structure for the database. Can run the class by specifying 'to_create' = True upon
# instantiation, or by running the .run_methods()
from s3_project.classes.create_database import ProjectDatabase
from s3_project.classes.joining_class import JoinCleanData

new = ProjectDatabase(to_create=False)  # Change value to true to create database
merged_df = JoinCleanData()

# import pandas as pd
# print(pd.read_pickle("./merged_dataframe.pkl").columns)
