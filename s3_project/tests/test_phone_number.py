from s3_project.classes.talent_csv_cleaning import TalentCsv

test_number = TalentCsv()

def test_phone_number():
    # Checking various combinations of numbers
    assert test_number.cleaning_phone_numbers("+44 (123) 4567890") == "+44 123 456 7890"
    assert test_number.cleaning_phone_numbers("=44-123-4567890") == "+44 123 456 7890"
    assert test_number.cleaning_phone_numbers("+44-123-4567890") == "+44 123 456 7890"
    assert test_number.cleaning_phone_numbers("441234567890") == "+44 123 456 7890"
    assert test_number.cleaning_phone_numbers("+-=-!4""!4123@@45!^67&890") == "+44 123 456 7890"

    assert test_number.cleaning_phone_numbers("01234567890") == "+44 123 456 7890"
    assert test_number.cleaning_phone_numbers("01234567890") == "+44 123 456 7890"

