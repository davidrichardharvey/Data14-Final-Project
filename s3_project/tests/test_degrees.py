from s3_project.classes.talent_csv_cleaning import TalentCsv
test = TalentCsv()

def test_degrees():
    assert test.replace_degree("1st") == "1"
    assert test.replace_degree("3rd") == "3"
    assert test.replace_degree("Pass") == "p"
    assert test.replace_degree("Merit") == "m"
    assert test.replace_degree("Distinction") == "d"
