# from s3_project.classes.cleaning_txt import talent_txt
# from s3_project.classes.academy_class import academy_dataframe
# from s3_project.classes.talent_csv_cleaning import monthly_talent_info
# from s3_project.classes.applicant_info_class import talent_applicant_info
#
#
# print(f"Applicant Info Data Frame: {talent_applicant_info.df_talent_json}")
# print(f"Talent Text Files Data Frame: {talent_txt.df}")
# print(f"Academy Data Frame: {academy_dataframe.cleaned_df}")
# print(f"Monthly Talent Data Frame: {monthly_talent_info.df_talent_csv}")


# from s3_project.classes.create_database import new
# new.create_table_no_keys()


from s3_project.classes.joining_class import JoinCleanData
import pandas as pd

test = JoinCleanData()

candidates_dummy = [{'trainer_first_name': 'Evie', 'trainer_last_name': 'Demetriou', 'inv_by_firstname': 'Juxhen', 'inv_by_lastname': 'Bica'},
                    {'trainer_first_name': 'Evdokia', 'trainer_last_name': 'Deme', 'inv_by_firstname': 'Juxh', 'inv_by_lastname': 'Bic'},
                    {'trainer_first_name': 'Ev', 'trainer_last_name': 'Dem', 'inv_by_firstname': 'Jux', 'inv_by_lastname': 'Bc'},
                    {'trainer_first_name': 'Evie', 'trainer_last_name': 'Demetriou', 'inv_by_firstname': 'J', 'inv_by_lastname': 'B'}]
df = pd.DataFrame(candidates_dummy)

#test.staff_roles_load()
print(list(test.staff_table_load(df)))
