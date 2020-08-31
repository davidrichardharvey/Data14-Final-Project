from s3_project.classes.talent_csv_cleaning import TalentCsv
import pandas as pd

test = TalentCsv()


def test_concat_date():
    # Test to see if a date is formatted correctly

    # Create a dictionary for test dataframe
    unformatted_data = {'invited_date': [23, 30, 11, 1, 7, None],
                        'month': ['Sep-19', 'Apr-19', 'Jun-19', 'Feb-19', 'Oct-19', None]}

    # Convert into a pandas dataframe and run it through the method
    df = pd.DataFrame(unformatted_data)
    df = test.concat_dates(df, 'invited_date', 'month')

    # Expected dataframe
    formatted_data = {'invited_date': ['2019/09/23', '2019/04/30', '2019/06/11', '2019/02/01', '2019/10/07', None]}
    df2 = pd.DataFrame(formatted_data)

    # Compare the sorted test dataframe and expected dataframe
    assert sorted(df) == sorted(df2)
