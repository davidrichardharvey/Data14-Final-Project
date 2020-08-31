from s3_project.classes.academy_class import Academy
import pandas as pd
import os

test = Academy()


def test_last_name():
    assert test.find_last_names(['John John', 'De', 'Van', 'Doe']) == [['John John'], ['De', 'Van', 'Doe', '']]
