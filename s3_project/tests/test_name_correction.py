from s3_project.classes.talent_csv_cleaning import TalentCsv
test = TalentCsv()


def test_name():
    assert test.change_invited_by('Bruno Bellbrook') == 'Bruno Belbrook'
    assert test.change_invited_by('Fifi Eton') == 'Fifi Etton'
