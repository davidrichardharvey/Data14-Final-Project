# from s3_project.classes.create_database import new

# from s3_project.classes.joining_class import clean_data
# print(clean_data.merged_df)

import pandas as pd

from s3_project.classes.academy_class import academy_dataframe
from s3_project.functions import third_merge

print(third_merge(pd.read_pickle("./dummy.pkl"), academy_dataframe.cleaned_df))
