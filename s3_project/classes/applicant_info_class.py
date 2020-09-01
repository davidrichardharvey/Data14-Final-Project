import json
import boto3
import pandas as pd
from datetime import datetime
from s3_project.classes.extraction_class import import_files
from s3_project.Config.config_manager import find_variable


def apply_split_name(object_dict):
    # Splits the name key of a dictionary into first and last name
    object_dict['first_name'], object_dict['last_name'] = split_name(object_dict['name'])
    object_dict.pop('name')
    return object_dict


def split_name(name):
    # Converts name into a first and last name
    common_last_names = find_variable("common_last_names", "LAST NAMES")
    name_list = name.title().split()
    first_name = ' '.join(name_list[:-1])
    last_name = name_list[-1]
    for name in name_list:
        if name in common_last_names and name_list.index(name) != 0:
            first_name = ' '.join(name_list[:name_list.index(name)])
            last_name = ' '.join(name_list[name_list.index(name):])
            break
    return [first_name, last_name]


def append_file(file, object_dict):
    # This method appends a text file the files with more than 2 names which are not names in the config file.
    if " " in list(object_dict['first_name']):
        with open(find_variable("issues", "ISSUE FILES"), "a") as ai:
            ai.writelines(f"Filename: {file},  Name: {object_dict['first_name']} {object_dict['last_name']},  "
                          f"Issue: Ambiguity in sorting names,  "
                          f"How Resolved: Ambiguous names put in first name\n")


def date_format(object_dict):
    # This method cleans the date column
    date = object_dict['date']
    date = date.replace('//', '/')
    object_dict['date'] = datetime.strptime(date, '%d/%M/%Y').strftime('%Y/%M/%d')
    return object_dict


def boolean_values(input_value):
    # Transforms an input to be a boolean value
    if input_value in ['Yes', 'Pass']:
        return True
    elif input_value in ['No', 'Fail']:
        return False


def change_boolean(object_dict):
    # Applies the boolean transformation to the appropriate columns
    for boolean_col in ['result', 'self_development', 'financial_support_self', 'geo_flex']:
        object_dict[boolean_col] = boolean_values(object_dict[boolean_col])
    return object_dict


class ApplicantInfoClean:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = find_variable("bucket_name")
        self.files = import_files.talent_json_list
        self.number_files = len(import_files.talent_json_list)
        self.df_talent_json = pd.DataFrame()
        self.clean_files()

    def clean_files(self):
        # Cleans each file and adds them to a dataframe
        talent_json_list = []
        file_count = 0
        for file in self.files:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=file)
            body = s3_object['Body'].read()
            object_dict = json.loads(body)
            apply_split_name(object_dict)
            append_file(file, object_dict)
            if 'tech_self_score' not in object_dict.keys():
                object_dict['tech_self_score'] = {}
            file_count += 1
            print(f"Getting data from {file}    {round(file_count/self.number_files * 100, 2)}% complete")
            object_dict = date_format(object_dict)
            object_dict = change_boolean(object_dict)
            talent_json_list.append(object_dict)
            if file_count == 500:
                break
        self.df_talent_json = pd.DataFrame(talent_json_list)


talent_applicant_info = ApplicantInfoClean()
