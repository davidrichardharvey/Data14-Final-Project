import json


def create_table_schema(table: dict, file_name: str = None):
    with open(file_name, 'w') as write_file:
        json.dump("", write_file)
    with open(file_name, 'a') as write_file:
        json.dump(table['Schema'], write_file)
