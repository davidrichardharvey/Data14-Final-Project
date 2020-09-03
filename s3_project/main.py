from s3_project.classes.create_database import new
print(new)
from s3_project.classes.identifier_df import testing

print(testing.df)

# from s3_project.classes.joining_class import merged_dfs
# df = merged_dfs.merged_df
#
# print(df['uni'])


# import pandas as pd
# pd.set_option('display.max_columns', None)
# df = pd.read_pickle("./merged_dataframe.pkl")
# print(df.reset_index(drop=True))
# for each in df['uni']:
#     if type(each) is not float:
#         if len(each) > 50:
#             print(each)
#

#testing.input_sql_tables()
# print(testing.Strengths)

#print(testing.identifier_df('course_id', 'course_name', 'course_name', testing.Courses, 'Courses'))
#print(testing.identifier_df('city_id', 'city', 'city', testing.Cities, 'Cities'))
#print(testing.Cities)

#testing.input_tables_to_sql()
# testing.apply_reassign()
# print(testing.df)

#print(testing.df)