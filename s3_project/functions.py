import json
import pandas as pd


def create_table_schema(table: dict, file_name: str = None):
    # Creates a JSON file containing the schema for all tables in the database
    with open(file_name, 'a') as write_file:
        json.dump(table, write_file)
        write_file.write("\n\n")


def first_merge(df1, df2):
    # Merges the monthly applicant info data frame onto the applicant info data frame
    print("Merging monthly applicant info onto the applicant info table")
    merged_df1 = pd.merge(df1, df2, how='outer', left_on=["first_name", "last_name", 'invited_date'],
                          right_on=['first_name', 'last_name', 'date'])
    return merged_df1


def second_merge(df1_2, df3):
    # Merges the previously merged data frame onto the sparta day text file data frame
    print("Merging each individual's JSON files onto the data frame")
    merged_df2 = pd.merge(df1_2, df3, how='outer',
                          left_on=["first_name", "last_name", 'invited_date'],
                          right_on=['first_name', 'last_name', 'date'])

    df3.to_pickle("./applicant_info.pkl")
    # Iterates through the data frame to find instances where names are repeated
    all_names = []
    duplicates = []
    for index, row in merged_df2.iterrows():
        name = f"{row[0]} {row[1]}"
        if name in all_names and name not in duplicates:
            duplicates.append(name)
        all_names.append(name)
    merged_df2['names'] = all_names

    # Creating a data frame for those that were not repeated
    new_df = merged_df2[~merged_df2['names'].isin(duplicates)]

    # Creating separate data frames for split entries and people with shared names
    same_name = []
    split_on_merge = []
    for person in duplicates:
        name_df = merged_df2[merged_df2['names'] == person]
        new_dict = {}

        # Checking the dates to see whether or not to keep different instances
        birth_dates = list(name_df['dob'])
        unis = list(name_df['uni'])
        unique_birth_dates = []
        unique_unis = []
        same_person = False
        for each in range(0, len(birth_dates)):
            if not pd.isna(birth_dates[each]) and birth_dates[each] not in unique_birth_dates:
                unique_birth_dates.append(birth_dates[each])
            if not pd.isna(unis[each]) and unis[each] not in unique_unis:
                unique_unis.append(unis[each])
            if len(unique_unis) == len(unique_birth_dates) == 1:
                same_person = True

        # If the person is the same person, need to merge their information
        if same_person:
            column_number = 0
            for column in name_df.columns:
                for index, row in name_df.iterrows():
                    value = row[column_number]
                    try:
                        is_null = pd.isna(value).all()
                    except AttributeError:
                        is_null = pd.isna(value)
                    if not is_null:
                        new_dict[column] = value
                column_number += 1
            split_on_merge.append(new_dict)
                # new_dict[list(name_df.columns)[column_number]] =
                # row[column_number]
                # new_dict[column] = ''
                # index = list(name_dict[column].keys())
                # for entry in index:
                #     if new_dict[column] == '':
                #         new_dict[column] = name_dict[column][entry]
                #     else:
                #         try:
                #             if not pd.isna(name_dict[column][entry]):
                #                 new_dict[column] = name_dict[column][entry]
                #         except ValueError:
                #             col_entry = name_dict[column][entry]
                #             if column in ['first_name', 'last_name']:
                #                 new_dict[column] = col_entry[list(col_entry.keys())[0]]
                #             if not pd.isna(pd.Series(name_dict[column][entry])).all():
                #                 if column in ['strengths', 'weaknesses']:
                #                     new_dict[column] = col_entry
                #                 else:
                #                     new_dict[column] = col_entry[list(col_entry.keys())[0]]


        # Producing a dictionary from the data frame of people with the same name
        else:
            same_name.append(name_df)

    # Creating data frames from list of dictionaries corresponding to the data in the table twice
    same_name_df = pd.concat(same_name)
    split_on_merge_df = pd.DataFrame(split_on_merge)

    # Altering the columns to remove the redundant columns and rename some to be more appropriate
    new_df = new_df.append([same_name_df, split_on_merge_df], sort=False)
    new_df.drop(['date_x', 'date_y', 'names'], inplace=True, axis=1)
    new_df.rename(columns={'invited_date': 'date'}, inplace=True)
    new_df.to_pickle("./dummy.pkl")
    return new_df


def third_merge(merged_df, new_df):
    # Merges the candidate scores onto the existing data frame
    print("Merging candidate scores onto the data frame")
    all_candidates = []
    duplicates = []
    for index, row in merged_df.iterrows():
        name = f"{row[0]} {row[1]}"
        name = name.strip()
        if name in all_candidates:
            duplicates.append(name)
        all_candidates.append(name)
    merged_df['names'] = all_candidates

    # Obtaining the names of candidates for which there are scores in the academy
    passing_candidates = []
    for index, row in new_df.iterrows():
        name = f"{row[0]} {row[1]}"
        name = name.strip()
        passing_candidates.append(name)
    new_df['names'] = passing_candidates

    # Slicing the data frames based on whether or not the applicant's name is in the list of names of those who passed
    unambiguous_df = merged_df[~merged_df['names'].isin(passing_candidates)]

    # Creates a new data frame for each of the passing candidates and adds it to the final data frame
    score_df_list = []
    for name in passing_candidates:
        name_df = merged_df[merged_df['names'] == name]
        if len(name_df) > 1:
            if not pd.isna(name_df['result']).any():
                name_df = name_df[name_df['result']]
            if len(name_df) > 1:
                with open('issues.txt', 'a') as write_file:
                    write_file.write(f"Name: {name},  Issue: Unable to process candidate due to repeated name,  "
                                     f"How Resolved: Dropped candidate from data to be added. To insert the candidate  "
                                     f"into the database, please insert their details directly")
        name_scores = new_df[new_df['names'] == name]
        if len(name_scores) > 1:
            with open('issues.txt', 'a') as write_file:
                write_file.write(f"Name: {name},  Issue: Multiple trainees with same name, cannot find a way to"
                                 f"differentiate,  How Resolved: Dropped candidate from data to be added. To "
                                 f"insert the candidate into the database, please insert their details directly")
        elif len(name_scores) == len(name_df) == 1:
            score_df_list.append(pd.merge(name_df, name_scores, how='outer', left_on='names', right_on='names'))

    score_df = pd.concat(score_df_list)
    score_df.rename(columns={'first_name_x': 'first_name', 'last_name_x': 'last_name'}, inplace=True)
    score_df.drop(['first_name_y', 'last_name_y', 'names'], axis=1, inplace=True)

    result = pd.concat([unambiguous_df, score_df])
    return result


def all_merges(df1, df2, df3, df4):
    merge1 = first_merge(df1, df2)
    merge2 = second_merge(merge1, df3)
    final_df = third_merge(merge2, df4)
    final_df.to_pickle("./merged_dataframe.pkl")
    return final_df
