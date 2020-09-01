from s3_project.classes.applicant_info_class import apply_split_name, date_format, boolean_values, change_boolean

dict_1 = {'name': 'Shaun Blake', 'date': '01/02/2019', 'result': 'Pass', 'self_development': 'No',
          'financial_support_self': 'Yes', 'geo_flex': 'Yes'}
dict_2 = {'name': 'Vincent van Goph', 'date': '23//01/2020', 'result': 'Fail', 'self_development': 'Yes',
          'financial_support_self': 'No', 'geo_flex': 'Yes'}
dict_3 = {'name': 'Harry James Daniel Peter', 'date': '12//08//2012', 'result': 'Pass', 'self_development': 'Yes',
          'financial_support_self': 'Yes', 'geo_flex': 'Yes'}


def test_apply_split_name():
    # Tests that the names are split up correctly
    assert apply_split_name(dict_1)['first_name'] == 'Shaun'
    assert apply_split_name(dict_2)['last_name'] == 'Van Goph'
    assert apply_split_name(dict_3)['last_name'] == 'Peter'


def test_date_format():
    # Tests if the dates formatted correctly
    assert date_format(dict_1)['date'] == '2019/02/01'
    assert date_format(dict_2)['date'] == '2020/01/23'
    assert date_format(dict_3)['date'] == '2012/08/12'


def test_boolean_values():
    # Tests that each of the boolean values gives the correct output
    assert boolean_values(dict_1['result'])
    assert not boolean_values(dict_1['self_development'])
    assert boolean_values(dict_1['financial_support_self'])
    assert boolean_values(dict_1['geo_flex'])
    assert not boolean_values(dict_2['result'])
    assert boolean_values(dict_2['self_development'])
    assert not boolean_values(dict_2['financial_support_self'])
    assert boolean_values(dict_2['geo_flex'])
    assert boolean_values(dict_3['result'])
    assert boolean_values(dict_3['self_development'])
    assert boolean_values(dict_3['financial_support_self'])
    assert boolean_values(dict_3['geo_flex'])


def test_change_boolean():
    # Asserts that change_boolean converts the required values to boolean values
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


