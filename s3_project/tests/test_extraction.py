import boto3
from s3_project.classes.extraction_class import ExtractFromS3
test = ExtractFromS3()


def test_extraction():
    # See if the length of each list is greater than zero
    assert len(test.talent_csv_list) > 0
    assert len(test.talent_json_list) > 0
    assert len(test.talent_txt_list) > 0
    assert len(test.academy_csv_list) > 0


def test_check_files():
    # Iterate through talent csv list and see if all files end in .csv
    for file in test.talent_csv_list:
        assert file.endswith('.csv')
    # Iterate through talent json list and see if all files end in .json
    for file in test.talent_json_list:
        assert file.endswith('.json')
    # Iterate through talent txt list and see if all files end in .txt
    for file in test.talent_txt_list:
        assert file.endswith('.txt')
    # Iterate through academy csv list and see if all files end in .csv
    for file in test.academy_csv_list:
        assert file.endswith('.csv')


def test_greater_than_one():
    # See if the length of the list isn't just one
    assert len(test.talent_csv_list) > 1
    assert len(test.talent_json_list) > 1
    assert len(test.talent_txt_list) > 1
    assert len(test.academy_csv_list) > 1


def test_file_verify():
    # Test for a file in talent csv list
    for file in test.talent_csv_list:
        assert file.find("April2019Applicants.csv")
    # Test for a file in talent json list
    for file in test.talent_json_list:
        assert file.find("10603.json")
    # Test for a file in talent txt list
    for file in test.talent_txt_list:
        assert file.find("Sparta Day 1 August 2019.txt")
    # Test for a file in academy csv list
    for file in test.academy_csv_list:
        assert file.find("Business_20_2019-02-11.csv")
