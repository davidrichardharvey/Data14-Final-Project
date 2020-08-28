import json
import boto3
import os
import pandas as pd
from datetime import datetime


from s3_project.classes.extraction_class import import_files
from s3_project.Config.config_manager import find_variable


class TalentCsv:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = find_variable("bucket_name")
        self.files = import_files.talent_csv_list
        self.df_talent_csv = pd.DataFrame()
        self.running_cleaner_methods()

    def running_cleaner_methods(self):
        # Iterating through list of csv's, accessing the Body to enable cleaning
        for index in self.files:
            obj = import_files.s3_client.get_object(
                Bucket=import_files.bucket_name,
                Key=index)
            df = pd.read_csv(obj['Body'])
            df = df.drop(columns='id')
            df['name'].apply(self.flag_name)
            df['email'].apply(self.email_valid)
            df['first_name'] = df['name'].apply(self.splitting_first_names)
            df['last_name'] = df['name'].apply(self.splitting_last_names)
            df['gender'] = df['gender'].apply(self.formatting_gender)
            df['dob'] = df['dob'].apply(self.dob_formatting)
            df['address'] = df['address'].apply(self.format_address)
            df['phone_number'] = df['phone_number'].apply(self.cleaning_phone_numbers)
            df['degree'] = df['degree'].apply(self.replace_degree)
            df = self.concat_dates(df, 'invited_date', 'month')
            df['invited_by'] = df['invited_by'].apply(self.change_invited_by)
            df = df[['first_name', 'last_name', 'gender', 'dob', 'email', 'city', 'address', 'postcode', 'phone_number',
                                                                        'uni', 'degree', 'invited_date', 'invited_by']]
            self.df_talent_csv = self.df_talent_csv.append(df, ignore_index=True)

    def cleaning_phone_numbers(self, phone):
        # Takes a phone number as an argument, changes format to fit our requirements
        if type(phone) is str:
            if phone.startswith('0'):
                phone.replace('0', '44', 1)
            phone_filter = filter(str.isdigit, phone)
            clean_phone = "".join(phone_filter)
            format_phone = clean_phone[:2] + ' ' + clean_phone[2:5] + ' ' + clean_phone[5:8] + ' ' + clean_phone[8:]
            format_phone = f'+{format_phone}'
            return format_phone
        else:
            return phone

    def splitting_first_names(self, name):
        # Splits a full name and returns all but the last name
        if type(name) is str:
            name = name.title()
            first_name = ' '.join(name.split(' ')[:-1])
            return first_name
        else:
            return name

    def splitting_last_names(self, name):
        # Splits a full name and returns only the last name
        if type(name) is str:
            name = name.title()
            last_name = name.split(' ')[-1]
            return last_name
        else:
            return name

    def formatting_gender(self, gender):
        # This assigns the gender to a single letter M or F
        if type(gender) is str:
            gender = gender.title()
            return gender[0]
        else:
            return gender

    def dob_formatting(self, date):
        # This formats the date in YYYY/MM/dd format
        if type(date) is str:
            date_format = '%d/%m/%Y'
            datetime_obj = datetime.strptime(date, date_format).strftime('%Y/%m/%d')
            return datetime_obj
        else:
            return date

    def concat_dates(self, df, day, month_year):
        # This takes in a data-frame, with the name of two columns and returns the data-frame with a concatenated
        # and formatted date
        df[day] = df[day].fillna(0)
        df[month_year] = df[month_year].fillna(0)
        df['new_date'] = df[day].astype(int).map(str) + ' ' + df[month_year].map(str)
        df['new_date'].replace({'0 0': None}, inplace=True)
        df['new_date'] = pd.to_datetime(df.new_date).dt.strftime('%Y/%m/%d')
        df['invited_date'] = df['new_date']
        df = df.drop(columns=['month', 'new_date'])
        return df

    def flag_name(self, name):
        # This flags the name if there are more than two first names
        if len(name.split(' ')) > 2:
            with open(find_variable("talent_csv_issues", "ISSUE FILES"), "a") as ai:
                ai.writelines(f"{name.title()}\n")

    def format_address(self, address):
        # This formats the addresses to lower case with each word capitalised
        if type(address) is str:
            return address.title()

    def email_valid(self, email):
        # Checks if the email address includes an @ symbol and the fields that don't are written to a text file
        if type(email) is str:
            if '@' not in email:
                with open("monthly_applicant_emails_edgecases.txt", "a") as ai:
                    ai.writelines(f"{email}\n")

    def replace_degree(self, degree):
        # This method checks and converts the degree to the desired format
        degree_dict = {'1st': '1', '3rd': '3', 'Pass': 'p', 'Merit': 'm', 'Distinction': 'd'}
        if degree in degree_dict.keys():
            return degree_dict[degree]
        else:
            return degree

    def change_invited_by(self, name):
        # This method checks and converts the names to the correct spelling
        name_dict = {'Bruno Bellbrook': 'Bruno Belbrook', 'Fifi Eton': 'Fifi Etton'}
        if name in name_dict.keys():
            return name_dict[name]
        else:
            return name


monthly_talent_info = TalentCsv()

