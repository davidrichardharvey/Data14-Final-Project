from s3_project.Config.config_manager import find_hidden_variable
import pyodbc
import pandas as pd

server = find_hidden_variable('server')
database = find_hidden_variable('database')
username = find_hidden_variable('username')
password = find_hidden_variable('password')
connection_string = "DRIVER={SQL Server};"
connection_string += f"SERVER={server};"
connection_string += f"DATABASE={database};"
connection_string += f"UID={username};"
connection_string += f"PWD={password}"
sparta = pyodbc.connect(connection_string)
cursor = sparta.cursor()

candidates_dummy = [{'candidate_id': 1, 'first_name': 'Juxhen', 'last_name': 'Bica', 'gender': 'M', 'uni_id': 12,
                    'degree_id': 14, 'invited_by': 5, 'self_dev': 1, 'geo_flex': 1, 'self_finance': 1, 'result': 1,
                    'course_interest_id': 10}, {'candidate_id': 2, 'first_name': 'Jade', 'last_name': 'Arthurs',
                    'gender': 'F', 'uni_id': 8, 'degree_id': 12, 'invited_by': 7, 'self_dev': 1, 'geo_flex': 1,
                    'self_finance': 1, 'result': 1, 'course_interest_id': 12}, {'candidate_id': 1,
                    'first_name': 'Mints', 'last_name': 'Shoe', 'gender': 'M', 'uni_id': 19, 'degree_id': 21,
                    'invited_by': 9, 'self_dev': 1, 'geo_flex': 1, 'self_finance': 1, 'result': 1,
                    'course_interest_id': 12}]

df = pd.DataFrame(candidates_dummy)

query1 = """
SELECT candidate_id FROM candidates
"""

attempt = cursor.execute(query1)
def test_attempt():
    for item
    assert list(attempt) == []

