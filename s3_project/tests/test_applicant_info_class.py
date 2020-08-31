from s3_project.classes.applicant_info_class import apply_split_name
from s3_project.classes.applicant_info_class import date_format
from s3_project.classes.applicant_info_class import boolean_values
from s3_project.classes.applicant_info_class import change_boolean
from s3_project.classes.applicant_info_class import create_dataframe

dict_1 = {'name': 'Shaun Blake', 'date': '01/02/2019', 'result': 'Pass', 'self_development': 'No',
          'financial_support_self': 'Yes', 'geo_flex': 'Yes'}
dict_2 = {'name': 'Vincent van Goph', 'date': '23//01/2020', 'result': 'Fail', 'self_development': 'Yes',
          'financial_support_self': 'No', 'geo_flex': 'Yes'}
dict_3 = {'name': 'Harry James Daniel Peter', 'date': '12//08//2012', 'result': 'Pass', 'self_development': 'Yes',
          'financial_support_self': 'Yes', 'geo_flex': 'Yes'}


# Tests that the names are split up correctly
def test_apply_split_name():
    assert apply_split_name(dict_1)['first_name'] == 'Shaun'
    assert apply_split_name(dict_2)['last_name'] == 'Van Goph'
    assert apply_split_name(dict_3)['last_name'] == 'Peter'


# Tests if the dates are in the correct format
def test_date_format():
    assert date_format(dict_1) == '2019/02/01'
    assert date_format(dict_2) == '2020/01/23'
    assert date_format(dict_3) == '2012/08/12'


def test_boolean_values():
    assert boolean_values(dict_1['result']) == True
    assert boolean_values(dict_1['self_development']) == False
    assert boolean_values(dict_1['financial_support_self']) == True
    assert boolean_values(dict_1['geo_flex']) == True
    assert boolean_values(dict_2['result']) == False
    assert boolean_values(dict_2['self_development']) == True
    assert boolean_values(dict_2['financial_support_self']) == False
    assert boolean_values(dict_2['geo_flex']) == True
    assert boolean_values(dict_3['result']) == True
    assert boolean_values(dict_3['self_development']) == True
    assert boolean_values(dict_3['financial_support_self']) == True
    assert boolean_values(dict_3['geo_flex']) == True


def test_change_boolean():
    dict_1a = change_boolean(dict_1)
    dict_2a = change_boolean(dict_2)
    dict_3a = change_boolean(dict_3)
    assert type(dict_1a['result']) == bool
    assert type(dict_1a['self_development']) == bool
    assert type(dict_1a['financial_support_self']) == bool
    assert type(dict_1a['geo_flex']) == bool
    assert type(dict_2a['result']) == bool
    assert type(dict_2a['self_development']) == bool
    assert type(dict_2a['financial_support_self']) == bool
    assert type(dict_2a['geo_flex']) == bool
    assert type(dict_3a['result']) == bool
    assert type(dict_3a['self_development']) == bool
    assert type(dict_3a['financial_support_self']) == bool
    assert type(dict_3a['geo_flex']) == bool


json_list = [dict_1, dict_2, dict_3]


def test_create_df():
    assert len(create_dataframe(json_list)) == 3
    assert len(create_dataframe(json_list).columns) == 7
    assert create_dataframe(json_list).shape == (3, 7)
