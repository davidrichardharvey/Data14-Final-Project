import pandas as pd
from s3_project.classes.cleaning_txt import talent_txt
# from s3_project.classes.academy_class import academy_dataframe
from s3_project.classes.talent_csv_cleaning import monthly_talent_info
from s3_project.classes.applicant_info_class import talent_applicant_info


class JoinCleanData:
    def __init__(self):
        self.sparta_day_txt = talent_txt.df
        self.monthly_applicant_csv = monthly_talent_info.df_talent_csv
        # self.academy_scores_csv = academy_dataframe.cleaned_df
        self.applicant_info_json = talent_applicant_info.df_talent_json
        self.merged_df = ''
        self.merged_dataframes()

    def merged_dataframes(self):
        # Merges each of the files together into 1 large database containing all of the data

        # Merges the monthly applicant info dataframe onto the applicant info dataframe
        merged_df1 = pd.merge(self.monthly_applicant_csv, self.sparta_day_txt, how='outer',
                              left_on=["first_name", "last_name", 'invited_date'],
                              right_on=['first_name', 'last_name', 'date'])

        # Merges the previously merged dataframe onto the sparta day text file dataframe
        merged_df2 = pd.merge(merged_df1, self.applicant_info_json, how='outer',
                              left_on=["first_name", "last_name", 'invited_date'],
                              right_on=['first_name', 'last_name', 'date'])

        # Iterates through the dataframe to find instances where names are repeated
        all_names = []
        duplicates = []
        not_duplicates = []
        for index, row in merged_df2.iterrows():
            name = row[0] + row[1]
            if name in all_names:
                duplicates.append(name)
            all_names.append(name)
        merged_df2['names'] = all_names

        # Creating a new list of names for which there was only 1 value
        for name in all_names:
            if name not in duplicates:
                not_duplicates.append(name)

        # Creating separate dataframes for each of the different required parts
        new_df = merged_df2[merged_df2['names'].isin(not_duplicates)]
        duplicate_dataframes = []
        new_dict = {}
        for person in duplicates:
            new_dict = {}
            new_person_df = merged_df2[merged_df2['names'] == person]
            new_person_dict = new_person_df.to_dict()
            for column in new_person_dict:
                entries = []
                for entry in new_person_dict[column]:
                    entries.append(entry)
                new_dict[column] = new_person_dict[column][entries[0]]
            duplicate_dataframes.append(new_dict)
            print(new_dict)
        print(pd.DataFrame(duplicate_dataframes, index=range(0, len(duplicates))))

        # Combines the non-nan columns and creates the dataframe




clean_data = JoinCleanData()
