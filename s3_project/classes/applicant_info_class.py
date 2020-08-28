import json
import boto3
import os
import pandas as pd
from datetime import datetime

# new_wd = os.getcwd()[:-19]
# os.chdir(new_wd)

from s3_project.classes.extraction_class import import_files
from s3_project.Config.config_manager import find_variable


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
                self.append_file(file)
            if 'tech_self_score' not in object_dict.keys():
                object_dict['tech_self_score'] = 0
            self.split_names(object_dict)
            self.date_format(object_dict)
            self.boolean_values(object_dict)
            talent_json_list.append(object_dict)
        self.create_dataframe(talent_json_list)
        self.df_talent_json = self.create_dataframe(talent_json_list)
        return talent_json_list

    def split_names(self, object_dict):
        # This method splits name into first_name and last_name,
        # if there's more than 2 names, every name but the last goes into the first_name column,
        # and the ones with more than 2 names get appended to a text file.
        name_list = object_dict['name'].split(' ')
        if len(name_list) > 2:
            object_dict['first_name'] = " ".join(name_list[:-1])
            object_dict['last_name'] = name_list[-1]
            object_dict.pop('name')
        elif len(name_list) == 2:
            object_dict['first_name'] = name_list[0]
            object_dict['last_name'] = name_list[-1]
            object_dict.pop('name')
        return [object_dict['first_name'], object_dict['last_name']]

    def append_file(self, file):
        # This method appends a text file.
        with open(find_variable("talent_json_issues", "ISSUE FILES"), "a") as ai:
            ai.writelines(f"{file}\n")

    def date_format(self, object_dict):
        # This method cleans the date column
        date = object_dict['date']
        date = date.replace('//', '/')
        object_dict['date'] = datetime.strptime(date, '%d/%M/%Y').strftime('%Y/%M/%d')
        return object_dict['date']

    def boolean_values(self, input_value):
        # Transforms an input to be a boolean value
        if input_value == 'Yes' or input_value == 'Pass':
            return True
        elif input_value == 'No' or input_value == 'Fail':
            return False

    def change_boolean(self, object_dict):
        # Applies the boolean transformation to the appropriate columns
        object_dict['result'] = self.boolean_values(object_dict['result'])
        object_dict['self_development'] = self.boolean_values(object_dict['self_development'])
        object_dict['financial_support_self'] = self.boolean_values(object_dict['financial_support_self'])
        object_dict['geo_flex'] = self.boolean_values(object_dict['geo_flex'])
        return [object_dict['result'], object_dict['self_development'], object_dict['financial_support_self'],
                object_dict['geo_flex']]

    def create_dataframe(self, talent_json_list):
        # Creates a dataframe with all the data
        df = pd.DataFrame(talent_json_list)
        return df


talent_applicant_info = ApplicantInfoClean()
