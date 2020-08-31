import boto3
import pandas as pd
from datetime import datetime

from s3_project.classes.extraction_class import import_files
from s3_project.Config.config_manager import find_variable


def date_format(item):
    # Formats the date into YYYY/mm/dd format
    date = datetime.strptime(item['date'], '%A %d %B %Y').strftime('%Y/%m/%d')
    item['date'] = date
    return item


def two_names_txt(name):
    # Append the instances where someone still has 2 first names to a text file
    if " " in list(name['first_name']):
        with open(find_variable("issues", "ISSUE FILES"), "a") as text_file:
            text_file.writelines(
                f"FileName: Sparta Day {' '.join(name['date'].split()[1:])}.txt,  "
                f"Name:{name['first_name']} {name['last_name']},  "
                f"Issue: Ambiguity in sorting names,  How Resolved: Ambiguous names put in first name\n")
    return name


def get_scores(item):
    # Splits the scores into achieved score and the maximum score possible; also formats the name to title casing
    psyc = item.pop('psyc').split('/')
    pres = item.pop('pres').split('/')
    name_filter = filter(lambda x: x.isalpha() or x.isspace() or x == "-", item['first_name'])
    name_clean = "".join(name_filter)
    item['first_name'] = name_clean.title()
    item['psychometric'] = int(psyc[0])
    item['psychometric_max'] = int(psyc[1])
    item['presentation'] = int(pres[0])
    item['presentation_max'] = int(pres[1].strip("']").strip('"'))
    return item


class TextFiles:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = find_variable('bucket_name')
        self.files = import_files.talent_txt_list
        self.file_contents = []
        self.results = []
        self.common_last_names = find_variable("common_last_names", "LAST NAMES")
        self.iterate_txt()
        self.split_name_results()
        self.iterate_files()
        self.df = pd.DataFrame(self.results)

    def iterate_txt(self):
        # Gets the information from the body of the txt file
        for file in self.files:
            s3_object = self.s3_client.get_object(Bucket=self.bucket_name, Key=file)
            body = s3_object['Body'].read()
            strbody = body.decode('utf-8').splitlines()
            self.file_contents.append({'date': strbody[0], 'location': strbody[1], 'results': strbody[3:]})
            print(f"Getting data from {file}")

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

    def apply_split_name(self, item):
        # Splits each of the names in all of the files imported
        name = item['name']
        item['first_name'], item['last_name'] = self.split_name(name)
        item.pop('name')
        return item

    def split_name(self, name):
        split_name = name.title().split()
        first_name = ' '.join(split_name[:-1]).title()
        last_name = split_name[-1].title()
        for name in split_name:
            if name in self.common_last_names and split_name.index(name) != 0:
                first_name = ' '.join(split_name[:split_name.index(name)]).title().strip('"').strip("'")
                last_name = ' '.join(split_name[split_name.index(name):]).title()
                break
        return [first_name, last_name]

    def iterate_files(self):
        for file in range(0, len(self.results)):
            self.results[file] = self.apply_split_name(self.results[file])
            self.results[file] = get_scores(self.results[file])
            self.results[file] = two_names_txt(self.results[file])
            self.results[file] = date_format(self.results[file])

talent_txt = TextFiles()

