from s3_project.classes.talent_csv_cleaning import TalentCsv
import os
test = TalentCsv()

def test_file_created():
    # Test to see if a file is created if the splitting of the name results in 2 first names
    test_name = 'John Van Doe'
    file = []
    test.flag_name(test_name, file)
    assert os.path.exists('./issues.txt')
