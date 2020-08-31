import json


def create_table_schema(table: dict, file_name: str = None):
    with open(file_name, 'a') as write_file:
        json.dump(table, write_file)
        write_file.write("\n\n")
