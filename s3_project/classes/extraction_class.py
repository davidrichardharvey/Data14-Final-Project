import boto3
from ..Config.config_manager import find_variable


class ExtractFromS3:
    def __init__(self):
        # Initialisation with lists to hold objects obtained from methods
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.bucket_list = self.s3_client.list_buckets()
        self.bucket_name = find_variable('bucket_name')
        self.bucket = self.s3_resource.Bucket(self.bucket_name)
        self.contents = self.bucket.objects.all()

        # Creating lists for storing separated file names
        self.academy_csv_list = []
        self.talent_csv_list = []
        self.talent_json_list = []
        self.talent_txt_list = []
        self.get_data()  # Running the method to extract files from S3

    def get_data(self):
        # Method to separate objects into lists in preparation for cleaning
        for obj in self.contents:  # Iterating through each object in each bucket
            object_key = obj.key
            if object_key.startswith('Talent'):
                if object_key.endswith('.csv'):  # To retrieve csv files in the Talent folder
                    self.talent_csv_list.append(object_key)
                elif object_key.endswith('.json'):  # To retrieve json files in the Talent folder
                    self.talent_json_list.append(object_key)
                elif object_key.endswith('.txt'):  # To retrieve txt files in the Talent folder
                    self.talent_txt_list.append(object_key)
            elif object_key.startswith('Academy'):
                if object_key.endswith('.csv'):  # To retrieve csv files in the Academy folder
                    self.academy_csv_list.append(object_key)


import_files = ExtractFromS3()
