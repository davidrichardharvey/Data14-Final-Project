from s3_project.classes.talent_csv_cleaning import TalentCsv
import os
test = TalentCsv()


def test_file_created():
    # Flags the files where the name contains 2 first names
    test_name = 'John John Doe'
    file = ['Test File']
    test.flag_name(test_name, file)
    assert os.path.exists('./issues.txt')
