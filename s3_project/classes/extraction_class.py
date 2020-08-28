import boto3


class ExtractFromS3:
    # Initialisation with lists to hold objects obtained from methods
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.bucket_list = self.s3_client.list_buckets()
        self.bucket_name = 'data14-engineering-project'
        self.bucket = self.s3_resource.Bucket(self.bucket_name)
        self.contents = self.bucket.objects.all()
        self.academy_csv_list = []  # Lists for storing separated objects
        self.talent_csv_list = []
        self.talent_json_list = []
        self.talent_txt_list = []
        self.get_data()

    # Method to separate objects into lists in preparation for cleaning
    def get_data(self):
        for obj in self.contents:  # Iterating through each object in each bucket
            object_key = obj.key
            if object_key.startswith('Talent'):
                if object_key.endswith('.csv'):  # To retrieve csv files in the Talent bucket
                    self.talent_csv_list.append(object_key)
                elif object_key.endswith('.json'):  # To retrieve json files in the Talent bucket
                    self.talent_json_list.append(object_key)
                elif object_key.endswith('.txt'):  # To retrieve txt files in the Talent bucket
                    self.talent_txt_list.append(object_key)
            elif object_key.startswith('Academy'):
                if object_key.endswith('.csv'):  # To retrieve csv files in the Academy bucket
                    self.academy_csv_list.append(object_key)