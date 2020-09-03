from s3_project.classes.cleaning_txt import talent_txt
from s3_project.classes.academy_class import academy_dataframe
from s3_project.classes.talent_csv_cleaning import monthly_talent_info
from s3_project.classes.applicant_info_class import talent_applicant_info
import pandas as pd
# print(f"Applicant Info Data Frame: {talent_applicant_info.df_talent_json}")
# print(f"Talent Text Files Data Frame: {talent_txt.df}")
# print(f"Academy Data Frame: {academy_dataframe.cleaned_df}")
# print(f"Monthly Talent Data Frame: {monthly_talent_info.df_talent_csv}")

from s3_project.classes.joining_class import clean_data

candidates_dummy = [{'candidate_id': 1, 'first_name': 'Juxhen', 'last_name': 'Bica', 'gender': 'M', 'uni_id': 12,
                     'degree_id': 14, 'invited_by': 5, 'self_dev': 1, 'geo_flex': 1, 'self_finance': 1, 'result': 1,
                     'course_interest_id': 10},
                    {'candidate_id': 2, 'first_name': 'Jade', 'last_name': 'Arthurs',
                     'gender': 'F', 'uni_id': 8, 'degree_id': 12, 'invited_by': 7,
                     'self_dev': 1, 'geo_flex': 1,
                     'self_finance': 1, 'result': 1, 'course_interest_id': 12},
                    {'candidate_id': 3,
                     'first_name': 'Mints', 'last_name': 'Shoe', 'gender': 'M', 'uni_id': 19, 'degree_id': 21,
                     'invited_by': 9, 'self_dev': 1, 'geo_flex': 1, 'self_finance': 1, 'result': 1,
                     'course_interest_id': 12}]

df = pd.DataFrame(candidates_dummy)

print(clean_data.candidates_load(df))
