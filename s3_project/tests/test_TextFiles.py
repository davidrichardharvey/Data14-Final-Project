from s3_project.classes.cleaning_txt import TextFiles
import os

test = TextFiles()


def test_iterate_txt():
    assert len(test.file_contents) == len(test.files)


def test_split_name_results():
    for i in test.results:
        assert type(i['first_name']) is str
        assert 'Academy' in i['location']
        assert ',' not in i['psyc']
        assert "'," not in i['pres']


def test_clean_scores_names():
    for i in test.split_list:
        assert i['psychometric_max'] == 100
        assert i['presentation_max'] == 32
        assert i['psychometrics'] <= 100
        assert i['presentation'] <= 32
        assert i['first_name'] == i['first_name'].title()
        assert i['last_name'] == i['last_name'].title()
        assert ']' not in i['last_name']


def test_date_format():
    for i in test.final_list:
        assert i['date'].startswith('20')
        assert len(i['date']) == 10


def test_two_names_txt():
    assert os.path.isfile('./issues.txt') is True


def test_to_dataframe():
    assert len(test.df.columns) == 8
    assert len(test.df) == len(test.final_list)
