import json


def create_table_schema(table_schema: dict, location: str = None):
    if location:
        file = f"{location}/{table_schema['Name']}_table.json"
    else:
        file = 'table_schema.json'
    with open(file, 'a') as write_file:
        json.dump(table_schema['Schema'], write_file)
