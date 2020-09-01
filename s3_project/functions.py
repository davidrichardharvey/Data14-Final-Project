import json


def create_table_schema(table: dict, file_name: str = None):
    # Creates a JSON file containing the schema for all tables in the database
    with open(file_name, 'a') as write_file:
        json.dump(table, write_file)
        write_file.write("\n\n")
