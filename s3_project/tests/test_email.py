from s3_project.classes.talent_csv_cleaning import TalentCsv
import os
test = TalentCsv()

def test_email_valid():
    # Test to see if the function returns an email if it does include '@'
    file = []
    assert test.email_valid('something@gmail.com', file)


def test_file_created():
    # Test to see if a file is created if the email does not contain an '@' symbol
    test_email = 'somethinggmail.com'
    file = []
    test.email_valid(test_email, file)
    assert os.path.exists('./issues.txt')
