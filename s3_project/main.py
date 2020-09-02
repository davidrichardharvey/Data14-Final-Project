# from s3_project.classes.create_database import new

from s3_project.classes.joining_class import clean_data
print(clean_data.merged_df)

pd.read_pickle("./merged_dataframe.plk")