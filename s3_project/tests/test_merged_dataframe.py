from s3_project.classes.joining_class import JoinCleanData
import pandas as pd

monthly_applicant_1 = {'first_name': 'Charlotte', 'last_name': 'Kings', 'gender': 'F', 'dob': '1997/08/17',
                       'email': '1@2.com', 'city': 'London', 'address': '64 Zoo Lane', 'postcode': 'CV12 4BU',
                       'phone_number': '+44 24 7662 7366', 'uni': 'Bath', 'degree': '1', 'invited_date': '2018/10/14',
                       'inv_by_firstname': 'Paula', 'inv_by_lastname': 'Kedra'}
monthly_applicant_2 = {'first_name': 'Katie', 'last_name': 'McDonnell', 'gender': 'F', 'dob': '1997/09/01',
                       'email': '1@2000.com', 'city': 'Edinburgh ', 'address': '53 Spot Street', 'postcode': 'ED9 5BH',
                       'phone_number': '+44 89 7592 8936', 'uni': 'Liverpool', 'degree': '1',
                       'invited_date': '2018/08/17', 'inv_by_firstname': 'Paula', 'inv_by_lastname': 'Kedra'}
df_monthly_applicant = pd.DataFrame([monthly_applicant_1, monthly_applicant_2])

sparta_day_1 = {'date': '2018/10/14', 'location': 'London', 'first_name': 'Charlotte', 'last_name': 'Kings',
                'psychometric': 63, 'psychometric_max': 100, 'presentation': 24, 'presentation_max': 32}
sparta_day_2 = {'date': '2018/08/17', 'location': 'London', 'first_name': 'Katie', 'last_name': 'McDonnell',
                'psychometric': 85, 'psychometric_max': 100, 'presentation': 16, 'presentation_max': 32}
df_sparta_day = pd.DataFrame([sparta_day_1, sparta_day_2])

first_merge_1 = {'first_name': 'Charlotte', 'last_name': 'Kings', 'gender': 'F', 'dob': '1997/08/17',
                 'email': '1@2.com',
                 'city': 'London', 'address': '64 Zoo Lane', 'postcode': 'CV12 4BU', 'phone_number': '+44 24 7662 7366',
                 'uni': 'Bath', 'degree': '1', 'invited_date': '2018/10/14', 'inv_by_firstname': 'Paula',
                 'inv_by_lastname': 'Kedra', 'location': 'London', 'psychometric': 63, 'psychometric_max': 100,
                 'presentation': 24, 'presentation_max': 32}
first_merge_2 = {'first_name': 'Katie', 'last_name': 'McDonnell', 'gender': 'F', 'dob': '1997/09/01',
                 'email': '1@5.com',
                 'city': 'Edinburgh ', 'address': '53 Spot Street', 'postcode': 'ED9 5BH',
                 'phone_number': '+44 89 7592 8936', 'uni': 'Liverpool', 'degree': '1', 'invited_date': '2018/08/17',
                 'inv_by_firstname': 'Paula', 'inv_by_lastname': 'Kedra', 'location': 'London', 'psychometric': 85,
                 'psychometric_max': 100, 'presentation': 16, 'presentation_max': 32}
df_first_merge = pd.DataFrame([first_merge_1, first_merge_2])


def test_first_merge():
    # Merge Monthly Applicant csv files and Sparta Day txt files
    assert first_merge(df_monthly_applicant, df_sparta_day) == df_first_merge

app_info_1 = {'date': '2018/10/14', 'tech_self_score': {'C#': 6, 'Java': 5, 'R': 2, 'JavaScript': 2},
              'strengths': ['Charisma'], 'weaknesses': ['Introverted', 'Distracted'], 'self_development': True,
              'geo_flex': False, 'financial_support_self': True, 'result': True, 'course_interest': 'engineering',
              'first_name': 'Charlotte', 'last_name': 'Kings'}
app_info_2 = {'date': '2018/08/17', 'tech_self_score': {'Java': 5, 'R': 2, 'JavaScript': 2},
              'strengths': ['Confident', 'Friendly'], 'weaknesses': ['Impulsive', 'Distracted'],
              'self_development': True, 'geo_flex': False, 'financial_support_self': True, 'result': True,
              'course_interest': 'engineering', 'first_name': 'Katie', 'last_name': 'McDonnell'}
df_app_info = pd.DataFrame([app_info_1, app_info_2])

second_merge_1 = {'first_name': 'Charlotte', 'last_name': 'Kings', 'gender': 'F', 'dob': '1997/08/17',
                  'email': '1@2.com', 'city': 'London', 'address': '64 Zoo Lane', 'postcode': 'CV12 4BU',
                  'phone_number': '+44 24 7662 7366', 'uni': 'Bath', 'degree': '1', 'invited_date': '2018/10/14',
                  'inv_by_firstname': 'Paula', 'inv_by_lastname': 'Kedra', 'location': 'London', 'psychometric': 63,
                  'psychometric_max': 100, 'presentation': 24, 'presentation_max': 32,
                  'tech_self_score': {'C#': 6, 'Java': 5, 'R': 2, 'JavaScript': 2}, 'strengths': ['Charisma'],
                  'weaknesses': ['Introverted', 'Distracted'], 'self_development': True, 'geo_flex': False,
                  'financial_support_self': True, 'result': True, 'course_interest': 'engineering'}
second_merge_2 = {'first_name': 'Katie', 'last_name': 'McDonnell', 'gender': 'F', 'dob': '1997/09/01',
                  'email': '1@5.com', 'city': 'Edinburgh ', 'address': '53 Spot Street', 'postcode': 'ED9 5BH',
                  'phone_number': '+44 89 7592 8936', 'uni': 'Liverpool', 'degree': '1', 'invited_date': '2018/08/17',
                  'inv_by_firstname': 'Paula', 'inv_by_lastname': 'Kedra', 'location': 'London', 'psychometric': 85,
                  'psychometric_max': 100, 'presentation': 16, 'presentation_max': 32,
                  'tech_self_score': {'Java': 5, 'R': 2, 'JavaScript': 2}, 'strengths': ['Confident', 'Friendly'],
                  'weaknesses': ['Impulsive', 'Distracted'], 'self_development': True, 'geo_flex': False,
                  'financial_support_self': True, 'result': True, 'course_interest': 'engineering'}
df_second_merge = pd.DataFrame([second_merge_1, second_merge_2])


def test_second_merge():
    # Merge Monthly Applicant csv files and Sparta Day txt files with applicant info json files
    assert second_merge(df_first_merge, df_app_info) == df_second_merge


stream_group_1 = {'first_name': 'Charlotte', 'last_name': 'Kings', 'trainer_first_name': 'David',
                  'trainer_last_name': 'Harvey', 'course_name': 'Data_22', 'course_start_date': '2019/05/15',
                  'Analytic_W1': 5, 'Independent_W1': 8, 'Determined_W1': 6, 'Professional_W1': 5, 'Studious_W1': 4,
                  'Imaginative_W1': 6, 'Analytic_W2': 3, 'Independent_W2': 5, 'Determined_W2': 8, 'Professional_W2': 7,
                  'Studious_W2': 6, 'Imaginative_W2': 7, 'Analytic_W3': 6, 'Independent_W3': 5, 'Determined_W3': 6,
                  'Professional_W3': 7, 'Studious_W3': 4, 'Imaginative_W3': 5, 'Analytic_W4': 3, 'Independent_W4': 8,
                  'Determined_W4': 7, 'Professional_W4': 7, 'Studious_W4': 6, 'Imaginative_W4': 5, 'Analytic_W5': 5,
                  'Independent_W5': 8, 'Determined_W5': 5, 'Professional_W5': 6, 'Studious_W5': 8, 'Imaginative_W5': 4,
                  'Analytic_W6': 7, 'Independent_W6': 6, 'Determined_W6': 5, 'Professional_W6': 7, 'Studious_W6': 6,
                  'Imaginative_W6': 5, 'Analytic_W7': 4, 'Independent_W7': 8, 'Determined_W7': 6, 'Professional_W7': 8,
                  'Studious_W7': 5, 'Imaginative_W7': 6, 'Analytic_W8': 7, 'Independent_W8': 8, 'Determined_W8': 4,
                  'Professional_W8': 7, 'Studious_W8': 8, 'Imaginative_W8': 4, 'Analytic_W9': 6, 'Independent_W9': 8,
                  'Determined_W9': 6, 'Professional_W9': 8, 'Studious_W9': 7, 'Imaginative_W9': 8, 'Analytic_W10': 7,
                  'Independent_W10': 6, 'Determined_W10': 7, 'Professional_W10': 6, 'Studious_W10': 7,
                  'Imaginative_W10': 8}
stream_group_2 = {'first_name': 'Katie', 'last_name': 'McDonnell', 'trainer_first_name': 'David',
                  'trainer_last_name': 'Harvey', 'course_name': 'Data_22', 'course_start_date': '2019/05/15',
                  'Analytic_W1': 5, 'Independent_W1': 3, 'Determined_W1': 4, 'Professional_W1': 2, 'Studious_W1': 4,
                  'Imaginative_W1': 6, 'Analytic_W2': 3, 'Independent_W2': 5, 'Determined_W2': 2, 'Professional_W2': 6,
                  'Studious_W2': 5, 'Imaginative_W2': 3}
df_stream_group = pd.DataFrame([stream_group_1, stream_group_2])
third_merge_1 = {'first_name': 'Charlotte', 'last_name': 'Kings', 'gender': 'F', 'dob': '1997/08/17',
                 'email': '1@2.com', 'city': 'London', 'address': '64 Zoo Lane', 'postcode': 'CV12 4BU',
                 'phone_number': '+44 24 7662 7366', 'uni': 'Bath', 'degree': '1', 'invited_date': '2018/10/14',
                 'inv_by_firstname': 'Paula', 'inv_by_lastname': 'Kedra', 'location': 'London', 'psychometric': 63,
                 'psychometric_max': 100, 'presentation': 24, 'presentation_max': 32,
                 'tech_self_score': {'C#': 6, 'Java': 5, 'R': 2, 'JavaScript': 2},
                 'strengths': ['Charisma'], 'weaknesses': ['Introverted', 'Distracted'], 'self_development': True,
                 'geo_flex': False, 'financial_support_self': True, 'result': True, 'course_interest': 'engineering',
                 'trainer_first_name': 'David', 'trainer_last_name': 'Harvey', 'course_name': 'Data_22',
                 'course_start_date': '2019/05/15', 'Analytic_W1': 5, 'Independent_W1': 8, 'Determined_W1': 6,
                 'Professional_W1': 5, 'Studious_W1': 4, 'Imaginative_W1': 6, 'Analytic_W2': 3, 'Independent_W2': 5,
                 'Determined_W2': 8, 'Professional_W2': 7, 'Studious_W2': 6, 'Imaginative_W2': 7, 'Analytic_W3': 6,
                 'Independent_W3': 5, 'Determined_W3': 6, 'Professional_W3': 7, 'Studious_W3': 4, 'Imaginative_W3': 5,
                 'Analytic_W4': 3, 'Independent_W4': 8, 'Determined_W4': 7, 'Professional_W4': 7, 'Studious_W4': 6,
                 'Imaginative_W4': 5, 'Analytic_W5': 5, 'Independent_W5': 8, 'Determined_W5': 5, 'Professional_W5': 6,
                 'Studious_W5': 8, 'Imaginative_W5': 4, 'Analytic_W6': 7, 'Independent_W6': 6, 'Determined_W6': 5,
                 'Professional_W6': 7, 'Studious_W6': 6, 'Imaginative_W6': 5, 'Analytic_W7': 4, 'Independent_W7': 8,
                 'Determined_W7': 6, 'Professional_W7': 8, 'Studious_W7': 5, 'Imaginative_W7': 6, 'Analytic_W8': 7,
                 'Independent_W8': 8, 'Determined_W8': 4, 'Professional_W8': 7, 'Studious_W8': 8, 'Imaginative_W8': 4,
                 'Analytic_W9': 6, 'Independent_W9': 8, 'Determined_W9': 6, 'Professional_W9': 8, 'Studious_W9': 7,
                 'Imaginative_W9': 8, 'Analytic_W10': 7, 'Independent_W10': 6, 'Determined_W10': 7,
                 'Professional_W10': 6, 'Studious_W10': 7, 'Imaginative_W10': 8}
third_merge_2 = {'first_name': 'Katie', 'last_name': 'McDonnell', 'gender': 'F', 'dob': '1997/09/01',
                 'email': '1@5.com', 'city': 'Edinburgh ', 'address': '53 Spot Street', 'postcode': 'ED9 5BH',
                 'phone_number': '+44 89 7592 8936', 'uni': 'Liverpool', 'degree': '1', 'invited_date': '2018/08/17',
                 'inv_by_firstname': 'Paula', 'inv_by_lastname': 'Kedra', 'location': 'London', 'psychometric': 85,
                 'psychometric_max': 100, 'presentation': 16, 'presentation_max': 32,
                 'tech_self_score': {'Java': 5, 'R': 2, 'JavaScript': 2}, 'strengths': ['Confident', 'Friendly'],
                 'weaknesses': ['Impulsive', 'Distracted'], 'self_development': True, 'geo_flex': False,
                 'financial_support_self': True, 'result': True, 'course_interest': 'engineering',
                 'trainer_first_name': 'David', 'trainer_last_name': 'Harvey', 'course_name': 'Data_22',
                 'course_start_date': '2019/05/15', 'Analytic_W1': 5, 'Independent_W1': 3, 'Determined_W1': 4,
                 'Professional_W1': 2, 'Studious_W1': 4, 'Imaginative_W1': 6, 'Analytic_W2': 3, 'Independent_W2': 5,
                 'Determined_W2': 2, 'Professional_W2': 6, 'Studious_W2': 5, 'Imaginative_W2': 3}
df_third_merge = pd.DataFrame([third_merge_1, third_merge_2])


def test_third_merge():
    # Merge Monthly Applicant csv files, Sparta Day txt files and applicant info json files with Stream Group csv files
    assert third_merge(df_second_merge, df_stream_group) == df_third_merge
