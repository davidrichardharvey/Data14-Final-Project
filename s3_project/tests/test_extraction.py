from s3_project.classes.extraction_class import ExtractFromS3
test = ExtractFromS3()


def test_extraction():
    # See if the length of each list is greater than zero
    assert len(test.talent_csv_list) > 0
    assert len(test.talent_json_list) > 0
    assert len(test.talent_txt_list) > 0
    assert len(test.academy_csv_list) > 0


def test_check_files():
    # Checking each of the files in the list are the correct file types
    for file in test.talent_csv_list:
        assert file.endswith('.csv')
    for file in test.talent_json_list:
        assert file.endswith('.json')
    for file in test.talent_txt_list:
        assert file.endswith('.txt')
    for file in test.academy_csv_list:
        assert file.endswith('.csv')


def test_greater_than_one():
    # See if the length of the list isn't just one
    assert len(test.talent_csv_list) > 1
    assert len(test.talent_json_list) > 1
    assert len(test.talent_txt_list) > 1
    assert len(test.academy_csv_list) > 1


def test_file_verify():
    # Test whether a file we know the name of ends in the correct list
    for file in test.talent_csv_list:
        assert file.find("April2019Applicants.csv")
    for file in test.talent_json_list:
        assert file.find("10603.json")
    for file in test.talent_txt_list:
        assert file.find("Sparta Day 1 August 2019.txt")
    for file in test.academy_csv_list:
        assert file.find("Business_20_2019-02-11.csv")
