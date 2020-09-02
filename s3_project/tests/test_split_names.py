from s3_project.classes.academy_class import Academy
import pandas as pd

test = Academy()


def test_split_names():
    # Create a test dataframe to run through the method
    data = {'input_col': ['Vikram Lennon', 'Cadi Ryder', 'Bianca Oneil', 'Brenden Romero',
                       'Elyse Rivers', 'Jolyon Gross', 'John Jr Doe']}
    df = pd.DataFrame(data)
    file_name = []

    # Run df through the method
    df = test.split_names('input_col', 'f_name_column_name', 'l_name_column_name', df, file_name)

    # Create an expected dataframe to match the test dataframe to
    expected_d = {'input_col': ['Vikram Lennon', 'Cadi Ryder', 'Bianca Oneil', 'Brenden Romero',
                                'Elyse Rivers', 'Jolyon Gross', 'John Jr Doe'],
                  'f_name_column_name': ['Vikram', 'Cadi', 'Bianca', 'Brenden', 'Elyse', 'Jolyon', 'John Jr'],
                  'l_name_column_name': ['Lennon', 'Ryder', 'Oneil', 'Romero', 'Rivers', 'Gross', 'Doe']}
    expected_df = pd.DataFrame(data=expected_d)

    assert sorted(df) == sorted(expected_df)
