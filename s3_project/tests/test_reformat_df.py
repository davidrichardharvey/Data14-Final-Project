from s3_project.classes.academy_class import Academy
import pandas as pd
import os

test = Academy()


def test_reformat_df():
    data = {'name': ['John Doe', 'Jane Doe'], 'trainer': ['David Harvey', 'David Harvey']}
    df = pd.DataFrame(data=data)
    filename = 'Data-39-2019-12-30.csv'

    df = test.reformat_dataframe(df, filename)

    expected_data = {'first_name': ['John', 'Jane'],
                  'last_name': ['Doe', 'Doe'], 'trainer_first_name': ['David', 'David'],
                  'trainer_last_name': ['Harvey', 'Harvey'], 'course_name': ['Data_39', 'Data_39'],
                  'course_start_date': ['2019 / 12 / 30', '2019 / 12 / 30']}
    expected_df = pd.DataFrame(data=expected_data)

    assert sorted(df) == sorted(expected_df)