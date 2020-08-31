from s3_project.classes.talent_csv_cleaning import TalentCsv
test = TalentCsv()

def test_format_address():
    # Test to see if an address is formatted correctly
    assert test.format_address('123 SOMETHING STREET') == '123 Something Street'
    assert test.format_address('123 something street') == '123 Something Street'
    assert test.format_address('0123 something street') == '0123 Something Street'
