from s3_project.classes.talent_csv_cleaning import TalentCsv
test = TalentCsv()

def test_first_name():
    # Test to see if the method returns the first name and any "middle" names capitalised
    # Regardless of formatting
    assert test.splitting_first_names('john doe') == 'John'
    assert test.splitting_first_names('John Doe') == 'John'
    assert test.splitting_first_names('JOHN DOE') == 'John'
    assert test.splitting_first_names('John Van Doe') == 'John Van'
    assert test.splitting_first_names('John Van De Doe') == 'John Van De'

def test_last_name():
    # Test to see if the method returns the last name only and capitalised
    # Regardless of formatting
    assert test.splitting_last_names('john doe') == 'Doe'
    assert test.splitting_last_names('John Doe') == 'Doe'
    assert test.splitting_last_names('John DOE') == 'Doe'
    assert test.splitting_last_names('John Van Doe') == 'Doe'
    assert test.splitting_last_names('John Van De Doe') == 'Doe'