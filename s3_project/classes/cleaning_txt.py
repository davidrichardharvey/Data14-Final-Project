import boto3
import pandas as pd
from datetime import datetime

from s3_project.classes.extraction_class import import_files
from s3_project.Config.config_manager import find_variable


class TextFiles:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = find_variable('bucket_name')
        self.files = import_files.talent_txt_list
        self.file_contents = []
        self.iterate_txt()
        self.results = []
        self.split_name_results()
        self.apply_split_name()
        self.split_list = []
        self.clean_scores_names()
        self.two_names_txt()
        self.final_list = []
        self.date_format()
        self.df = ""
        self.to_dataframe()

    def iterate_txt(self):
        # Splits a text file by row and adds the information to a list
        for i in self.files:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=i)
            body = s3_object['Body'].read()
            strbody = body.decode('utf-8').splitlines()
            self.file_contents.append({'date': strbody[0], 'location': strbody[1], 'results': strbody[3:]})

    def split_name_results(self):
        # Splits the name and results string to first_name, last_name, psychometric, presentation
        for item in self.file_contents:
            split = str(item['results']).split("',")
            for person in split:
                person_split = person.split()
                psyc_index = person_split.index('Psychometrics:')
                self.results.append({'name': " ".join(person_split[0:psyc_index - 1]).title()
                                        , 'date': item["date"], 'location': item["location"]
                                        , 'psyc': person_split[psyc_index + 1].strip(','),
                                     'pres': person_split[psyc_index + 3].strip("',")})

    def apply_split_name(self):
        for item in self.results:
            name = item['name']
            item['first_name'] = self.split_name(name)[0]
            item['last_name'] = self.split_name(name)[1]
            item.pop('name')

    def split_name(self, name):
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

    def clean_scores_names(self):
        # Splits the presentation and psychometric scores into score and max scores, also formats the name to title casing
        for item in self.results:
            psyc = item['psyc'].split('/')
            pres = item['pres'].split('/')
            name_filter = filter(lambda x: x.isalpha() or x.isspace(), item['first_name'])
            name_clean = "".join(name_filter)
            self.split_list.append({'first_name': name_clean.title(), 'last_name': item['last_name'].title().strip(']')
                                       , 'date': item['date'], 'location': item['location'],
                                    'psychometrics': int(psyc[0])
                                       , 'psychometric_max': int(psyc[1]), 'presentation': int(pres[0])
                                       , 'presentation_max': int(pres[1].strip("']").strip('"'))})

    def two_names_txt(self):
        # Append the 2 name names to a text file
        for name in self.split_list:
            if " " in list(name['first_name']):
                with open(find_variable("issues", "ISSUE FILES"), "a") as text_file:
                    text_file.writelines(
                        f"FileName: Sparta Day {' '.join(name['date'].split()[1:])}.txt,  "
                        f"Name:{name['first_name']} {name['last_name']},  "
                        f"Issue: Ambiguity in sorting names,  How Resolved: Ambiguous names put in first name\n")

    def date_format(self):
        # Formats the date into YYYY/mm/dd format
        for item in self.split_list:
            date = datetime.strptime(item['date'], '%A %d %B %Y').strftime('%Y/%m/%d')
            self.final_list.append({'first_name': item['first_name'], 'last_name': item['last_name'], 'date': date
                                       , 'location': item['location'], 'psychometrics': item['psychometrics']
                                       , 'psychometric_max': item['psychometric_max'],
                                    'presentation': item['presentation']
                                       , 'presentation_max': item['presentation_max']})

    def to_dataframe(self):
        self.df = pd.DataFrame(self.final_list)
        return self.df


talent_txt = TextFiles()
