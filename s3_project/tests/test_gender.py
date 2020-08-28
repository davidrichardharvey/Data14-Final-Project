from s3_project.classes.talent_csv_cleaning import TalentCsv
test_gender = TalentCsv()

def test_male():
    # Testing different ways of male to see if they all return "M"
    assert test_gender.formatting_gender("male") == "M"
    assert test_gender.formatting_gender("Male") == "M"
    assert test_gender.formatting_gender("MALE") == "M"

def test_female():
    # Testing different ways of male to see if they all return "M"
    assert test_gender.formatting_gender("female") == "F"
    assert test_gender.formatting_gender("Female") == "F"
    assert test_gender.formatting_gender("FEMALE") == "F"