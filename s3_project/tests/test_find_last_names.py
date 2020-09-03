from s3_project.classes.academy_class import Academy
test = Academy()


def test_last_name():
    # Check that the last names are placed correctly
    assert test.find_last_names(['John John', 'De', 'Van', 'Doe']) == [['John John'],
                                                                       ['De', 'Van', 'Doe', '']]
