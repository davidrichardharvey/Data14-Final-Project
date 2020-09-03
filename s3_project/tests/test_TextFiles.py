from s3_project.classes.cleaning_txt import TextFiles
import os
test = TextFiles()  # Tests for the TextFiles class designed to clean all the talent txt files


def test_iterate_txt():
    #  Testing to see that the file_contents is correctly taking the data from the files
    assert len(test.file_contents) == len(test.files)


def test_split_name_results():
    # Testing to see that the name in each file is splitting correctly and that the data is stored in the correct format
    for column in test.results:
        assert type(column['first_name']) is str
        assert 'Academy' in column['location']
        assert type(column['psychometric']) is int
        assert type(column['presentation']) is int


def test_get_scores():
    # Testing to see that the values for each key are clean and in the format we need
    for column in test.results:
        assert column['psychometric_max'] == 100
        assert column['presentation_max'] == 32
        assert column['psychometric'] <= 100
        assert column['presentation'] <= 32
        assert column['first_name'] == column['first_name'].title()
        assert column['last_name'] == column['last_name'].title()
        assert ']' not in column['last_name']


def test_date_format():
    # Testing to see that the dates are consistently clean and in the same format
    for column in test.results:
        assert column['date'].startswith('20')
        assert len(column['date']) == 10


def test_two_names_txt():
    # Testing that the issues.txt file is being created when the class is run
    assert os.path.isfile('./issues.txt') is True
