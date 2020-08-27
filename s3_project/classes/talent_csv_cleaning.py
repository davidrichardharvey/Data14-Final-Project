from s3_project.classes.ExtractionClass import ExtractFromS3
import pandas as pd
import datetime


class TalentCsv(ExtractFromS3):
    def __init__(self):
        # Inherited Extraction class, ran method to get data
        super().__init__()
        self.df_talent_csv = pd.DataFrame()
        self.running_cleaner_methods()


    def running_cleaner_methods(self):
        # Iterating through list of csv's, accessing the Body to enable cleaning
        for index in self.talent_csv_list:
            obj = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=index)
            df = pd.read_csv(obj['Body'])
            df = df.drop(columns='id')
            df['first_name'] = df['name'].apply(self.splitting_first_names)
            df['last_name'] = df['name'].apply(self.splitting_last_names)
            df['gender'] = df['gender'].apply(self.formatting_gender)
            df['dob'] = df['dob'].apply(self.dob_formatting)
            df['phone_number'] = df['phone_number'].apply(self.cleaning_phone_numbers)
            df = self.concat_dates(df, 'invited_date', 'month')
            df['invited_date'] = df['new_date']
            df = df.drop(columns=['month', 'new_date'])
            df['invited_by'] = df['invited_by'].replace({'Bruno Bellbrook': 'Bruno Belbrook', 'Fifi Eton': 'Fifi Etton'})
            df_talent_csv = self.df_talent_csv.append(df, ignore_index=True)
            self.df_talent_csv = df_talent_csv
        print(self.df_talent_csv[['invited_date', 'invited_by']])


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
        if type(gender) is str:
            gender = gender.title()
            return gender[0]
        else:
            return gender

    def dob_formatting(self, date):
        if type(date) is str:
            date_format = '%d/%m/%Y'
            datetime_obj = datetime.datetime.strptime(date, date_format).strftime('%Y/%m/%d')
            return datetime_obj
        else:
            return date

    def changing_day_type(self, num):
        if type(num) is float:
            num = str(num)
            num = num.strip(num[-2:])
            return num

    def concat_dates(self, df, day, month_year):
        df[day] = df[day].fillna(0)
        df[month_year] = df[month_year].fillna(0)
        df['new_date'] = df[day].astype(int).map(str) + ' ' + df[month_year].map(str)
        df['new_date'].replace({'0 0': None}, inplace=True)
        df['new_date'] = pd.to_datetime(df.new_date).dt.strftime('%Y/%m/%d')
        # df = df.drop(columns=[day, month_year, 'new_date'])
        return df

test = TalentCsv()



