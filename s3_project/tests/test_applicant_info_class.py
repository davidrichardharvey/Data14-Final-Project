from s3_project.classes.applicant_info_class import ApplicantInfoClean

dict_1 = {'name': 'Shaun Blake', 'date': '01/02/2019', 'result': 'Pass', 'self_development': 'No', 'financial_support_self': 'Yes', 'geo_flex':'Yes'}
dict_2 = {'name': 'Vincent van Goph', 'date':'23//01/2020', 'result': 'Fail', 'self_development': 'Yes', 'financial_support_self': 'No', 'geo_flex':'Yes'}
dict_3 = {'name': 'Harry James Daniel Peter', 'date':'12//08//2012', 'result': 'Pass', 'self_development': 'Yes', 'financial_support_self': 'Yes', 'geo_flex':'Yes'}

testing = ApplicantInfoClean()


# Tests that the names are split up correctly
def test_split_names():
    assert testing.split_names(dict_1) == ['Shaun', 'Blake']
    assert testing.split_names(dict_2) == ['Vincent van', 'Goph']
    assert testing.split_names(dict_3) == ['Harry James Daniel', 'Peter']


test_split_names()


# Tests if the dates are in the correct format
def test_date_format():
    assert testing.date_format(dict_1) == '2019/02/01'
    assert testing.date_format(dict_2) == '2020/01/23'
    assert testing.date_format(dict_3) == '2012/08/12'


test_date_format()


def test_boolean_values():
    assert testing.boolean_values(dict_1['result']) == True
    assert testing.boolean_values(dict_1['self_development']) == False
    assert testing.boolean_values(dict_1['financial_support_self']) == True
    assert testing.boolean_values(dict_1['geo_flex']) == True
    assert testing.boolean_values(dict_2['result']) == False
    assert testing.boolean_values(dict_2['self_development']) == True
    assert testing.boolean_values(dict_2['financial_support_self']) == False
    assert testing.boolean_values(dict_2['geo_flex']) == True
    assert testing.boolean_values(dict_3['result']) == True
    assert testing.boolean_values(dict_3['self_development']) == True
    assert testing.boolean_values(dict_3['financial_support_self']) == True
    assert testing.boolean_values(dict_3['geo_flex']) == True


test_boolean_values()
#
# result_type = isinstance(bool(dict_1['result']), bool)
# if result_type:
#     print("Test passed")
# else:
#     print("Test failed")
#
# print(type(bool(dict_1['result'])))
