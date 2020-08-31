import json
import boto3
import os
import pandas as pd
from datetime import datetime

from s3_project.classes.extraction_class import import_files
from s3_project.Config.config_manager import find_variable


def apply_split_name(object_dict):
        name = object_dict['name']
        object_dict['first_name'] = split_name(name)[0]
        object_dict['last_name'] = split_name(name)[1]
        object_dict.pop('name')


def split_name(name):
    common_last_names = find_variable("common_last_names", "LAST NAMES")
    split_name = name.title().split()
    first_name = ''
    last_name = ''
    for name in split_name:
        if name in common_last_names:
            first_name = ' '.join(split_name[:split_name.index(name)])
            last_name = ' '.join(split_name[split_name.index(name):])
            return [first_name, last_name]
        else:
            first_name = ' '.join(split_name[:-1])
            last_name = split_name[-1]
    return [first_name, last_name]


def append_file(file, object_dict):
    # This method appends a text file the files with more than 2 names which are not names in the config file.
    if " " in list(object_dict['first_name']):
        with open(find_variable("issues", "ISSUE FILES"), "a") as ai:
            ai.writelines(f"Filename is: {file}  first name: {object_dict['first_name']}  last name: {object_dict['last_name']} date: {object_dict['date']}\n")


def date_format(object_dict):
    # This method cleans the date column
    date = object_dict['date']
    date = date.replace('//', '/')
    object_dict['date'] = datetime.strptime(date, '%d/%M/%Y').strftime('%Y/%M/%d')
    return object_dict['date']


def boolean_values(input_value):
    # Transforms an input to be a boolean value
    if input_value == 'Yes' or input_value == 'Pass':
        return True
    elif input_value == 'No' or input_value == 'Fail':
        return False


def create_dataframe(talent_json_list):
    # Creates a dataframe with all the data
    df = pd.DataFrame(talent_json_list)
    return df


def change_boolean(object_dict):
    # Applies the boolean transformation to the appropriate columns
    object_dict['result'] = boolean_values(object_dict['result'])
    object_dict['self_development'] = boolean_values(object_dict['self_development'])
    object_dict['financial_support_self'] = boolean_values(object_dict['financial_support_self'])
    object_dict['geo_flex'] = boolean_values(object_dict['geo_flex'])
    return [object_dict['result'], object_dict['self_development'], object_dict['financial_support_self'],
            object_dict['geo_flex']]


class ApplicantInfoClean:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = find_variable("bucket_name")
        self.files = import_files.talent_json_list
        self.clean_files()
        self.df_talent_json = pd.DataFrame()

    def clean_files(self):
        # This method iterates through each file, and applies the cleaning methods to each file.
        # This method also appends the cleaned files to a dictionary.
        talent_json_list = []
        for file in self.files:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=file)
            body = s3_object['Body'].read()
            object_dict = json.loads(body)
            if len(object_dict['name'].split(' ')) > 2:
                apply_split_name(object_dict)
                append_file(file, object_dict)
            else:
                apply_split_name(object_dict)
            if 'tech_self_score' not in object_dict.keys():
                object_dict['tech_self_score'] = 0
            print(f"{file} is being cleaned")
            date_format(object_dict)
            boolean_values(object_dict)
            talent_json_list.append(object_dict)
        self.df_talent_json = create_dataframe(talent_json_list)
        return self.df_talent_json


talent_applicant_info = ApplicantInfoClean()
