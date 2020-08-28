import pandas as pd
import os
import boto3
from s3_project.classes.extraction_class import import_files
from s3_project.Config.config_manager import find_variable


class Academy:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.files = import_files.academy_csv_list
        self.issue_files = find_variable('issues', 'ISSUE FILES')
        self.common_last_names = find_variable('common_last_names', 'LAST NAMES')
        self.cleaned_df = self.get_cleaned_df()

    def append_to_txt_file(self, name, file_name):
        # Writes ambiguous names into a text file
        with open(self.issue_files, "a") as text_file:
            text_file.writelines(f"Filename: {file_name},  Name: {' '.join(name)},  Issue: Ambiguity in sorting names"
                                 f",  How Resolved: Ambiguous names put in first name\n")

    def split_names(self, input_col, f_name_column_name, l_name_column_name, df, file_name):
        # Splits a name column into first and last names then adds it to the dataframe
        first_names = []
        last_names = []
        common_last_names = find_variable('common_last_names', 'LAST NAMES').split(',')
        for index, row in df.iterrows():
            name_split = row[input_col].split()
            first_name, last_name = self.find_last_names(name_split)
            if len(first_name) >= 2:
                self.append_to_txt_file(name_split, file_name)
            first_names.append(' '.join(first_name))
            last_names.append(' '.join(last_name))
        df[f_name_column_name] = first_names
        df[l_name_column_name] = last_names
        return df

    def reformat_dataframe(self, df, file_name):
        # Re-formats the dataframes to place the scores at the end of the dataframe and apply the name splits
        behaviours = ["Analytic", "Independent", "Determined", "Professional", "Studious", "Imaginative"]
        course_duration = (len(list(df.columns)) - 4) / len(behaviours)
        course_weeks = range(1, int(course_duration) + 1)
        df = self.split_names('name', 'first_name', 'last_name', df, file_name)
        df = self.split_names('trainer', 'trainer_first_name', 'trainer_last_name', df, file_name)
        column_names = ["first_name", "last_name", "trainer_first_name", "trainer_last_name", 'course_name',
                        'course_start_date']
        for week in course_weeks:
            for kpi in behaviours:
                column_names.append(f'{kpi}_W{week}')
        df = df.reindex(columns=column_names)
        return df

    def get_cleaned_df(self):
        # Iterates through the file names and adds their re-formated data to a dataframe
        df_list = []
        for file_name in self.files:
            print(f"Getting data from {file_name}")
            s3_object = self.s3_client.get_object(
                Bucket='data14-engineering-project',
                Key=file_name)
            df = pd.read_csv(s3_object['Body'])
            file_name_split = file_name.split('_')
            df['course_name'] = f"{file_name_split[0].split('/')[1]}{file_name_split[1]}"
            df['course_start_date'] = file_name_split[2].split('.')[0].replace('-', '/')
            df_list.append(self.reformat_dataframe(df, file_name))
        return pd.concat(df_list)

    def find_last_names(self, name_split):
        # Finds the part of the name that is the last name, taking suffixes and common last names into account
        suffix = ""
        if name_split[-1] in find_variable('common_suffixes', 'LAST NAMES'):
            suffix = name_split.pop(-1)
        starting_last_name = [len(name_split) - 1]
        if len(name_split) >= 3:
            for each_name in name_split:
                if each_name.capitalize() in self.common_last_names:
                    starting_last_name.append(name_split.index(each_name))
        first_name = name_split[:min(starting_last_name)]
        last_name = name_split[min(starting_last_name):] + [suffix]
        return [first_name, last_name]


academy_dataframe = Academy()
