from s3_project.functions import all_merges
from s3_project.classes.academy_class import Academy
from s3_project.classes.talent_csv_cleaning import TalentCsv
from s3_project.classes.cleaning_txt import TextFiles
from s3_project.classes.applicant_info_class import ApplicantInfoClean


academy_dataframe = Academy()
monthly_talent_info = TalentCsv()
talent_txt = TextFiles()
talent_applicant_info = ApplicantInfoClean()


class JoinCleanData:
    def __init__(self):
        self.sparta_day_txt = talent_txt.df
        self.monthly_applicant_csv = monthly_talent_info.df_talent_csv
        self.academy_scores_csv = academy_dataframe.cleaned_df
        self.applicant_info_json = talent_applicant_info.df_talent_json
        self.merged_df = all_merges(self.monthly_applicant_csv, self.sparta_day_txt, self.applicant_info_json,
                                    self.academy_scores_csv)
