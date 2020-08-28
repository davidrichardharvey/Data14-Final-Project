# from s3_project.classes.cleaning_txt import talent_txt
# from s3_project.classes.academy_class import academy_dataframe
from s3_project.classes.talent_csv_cleaning import monthly_talent_info
# from s3_project.classes.applicant_info_class import talent_applicant_info
import pandas as pd
pd.set_option('display.max_rows', monthly_talent_info.df_talent_csv.shape[0]+1)


# print(f"Applicant Info Data Frame: {talent_applicant_info.create_dataframe(talent_applicant_info.clean_files())}")
# print(f"Talent Text Files Data Frame: {talent_txt.to_dataframe()}")
# print(f"Academy Data Frame: {academy_dataframe.cleaned_df}")
print(f"Monthly Talent Data Frame: {monthly_talent_info.df_talent_csv[['name', 'first_name', 'last_name']]}")


