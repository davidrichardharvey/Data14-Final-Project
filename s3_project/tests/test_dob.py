from s3_project.classes.talent_csv_cleaning import TalentCsv
test = TalentCsv()

def test_date_format():
    # Test to see if date is formatted properly in YYYY/mm/DD
    assert test.dob_formatting("26/07/1999") == "1999/07/26"
    assert test.dob_formatting("1/1/2020") == "2020/01/01"
    assert test.dob_formatting("01/1/2016") == "2016/01/01"
    assert test.dob_formatting("1/01/2016") == "2016/01/01"
