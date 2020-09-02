import json
import pandas as pd


def create_table_schema(table: dict, file_name: str = None):
    # Creates a JSON file containing the schema for all tables in the database
    with open(file_name, 'a') as write_file:
        json.dump(table, write_file)
        write_file.write("\n\n")


def first_merge(df1, df2):
    print("Merging monthly applicant info onto the applicant info table")
    # Merges the monthly applicant info dataframe onto the applicant info dataframe
    merged_df1 = pd.merge(df1, df2, how='outer', left_on=["first_name", "last_name", 'invited_date'],
                          right_on=['first_name', 'last_name', 'date'])
    print(merged_df1.columns)
    return merged_df1


def second_merge(df1_2, df3):
    print("Merging each individual's JSON files onto the data frame")
    # Merges the previously merged dataframe onto the sparta day text file dataframe
    merged_df2 = pd.merge(df1_2, df3, how='outer',
                          left_on=["first_name", "last_name", 'invited_date'],
                          right_on=['first_name', 'last_name', 'date'])

    # Iterates through the dataframe to find instances where names are repeated
    all_names = []
    duplicates = []
    for index, row in merged_df2.iterrows():
        name = f"{row[0]} {row[1]}"
        if name in all_names:
            duplicates.append(name)
        all_names.append(name)
    merged_df2['names'] = all_names

    # Creating a dataframe for those that were not repeated
    new_df = merged_df2[~merged_df2['names'].isin(duplicates)]

    # Creating separate dataframes for split entries and people with shared names
    same_name = []
    split_on_merge = []
    for person in duplicates:
        name_df = merged_df2[merged_df2['names'] == person]

        # Checking the dates to see whether or not to keep different instances
        birth_dates = list(name_df['dob'])
        unis = list(name_df['uni'])
        same_person = False
        for each in range(0, len(birth_dates)):
            if len(birth_dates) == len(unis) > 0:
                if birth_dates.count(birth_dates[0]) == len(birth_dates) and unis.count(unis[0]):
                    same_person = True

        # If the person is the same person, need to merge their information
        if same_person:
            name_dict = name_df.to_dict()
            new_dict = {}
            for column in name_dict:
                new_dict[column] = ''
                index = list(name_dict[column].keys())
                for entry in index:
                    if new_dict[column] == '':
                        new_dict[column] = name_dict[column][entry]
                    else:
                        try:
                            if not pd.isna(name_dict[column][entry]):
                                new_dict[column] = name_dict[column][entry]
                        except ValueError:
                            if column in ['first_name', 'last_name']:
                                new_dict[column] = name_dict[column][entry][name_dict[column][entry].keys()[0]]
                            if not pd.isna(pd.Series(name_dict[column][entry])).all():
                                if column in ['strengths', 'weaknesses']:
                                    new_dict[column] = name_dict[column][entry]
                                else:
                                    new_dict[column] = name_dict[column][entry][list(name_dict[column][entry].keys())[0]]

            split_on_merge.append(new_dict)

        # Producing a dictionary from the dataframe of people with the same name
        else:
            same_name.append(name_df.to_dict())

    # Creating dataframes from list of dictionaries corresponding to the data in the table twice
    same_name_df = pd.DataFrame(same_name)
    split_on_merge_df = pd.DataFrame(split_on_merge)

    # Altering the columns to remove the redundant columns and rename some to be more appropriate
    new_df = new_df.append([same_name_df, split_on_merge_df], sort=False)
    new_df.drop(['date_x', 'date_y', 'names'], inplace=True, axis=1)
    new_df.rename(columns={'invited_date': 'date'}, inplace=True)
    print(merged_df2.columns)
    return new_df


def third_merge(merged_df, new_df):
    print("Merging candidate scores onto the data frame")
    all_candidates = []
    for index, row in merged_df.iterrows():
        name = f"{row[0]} {row[1]}"
        name = name.strip()
        all_candidates.append(name)
    merged_df['names'] = all_candidates

    # Obtaining the names of candidates for which there are scores in the academy
    passing_candidates = []
    for index, row in new_df.iterrows():
        name = f"{row[0]} {row[1]}"
        name = name.strip()
        passing_candidates.append(name)
    new_df['names'] = passing_candidates


    print(all_candidates)
    # Slicing the dataframes based on whether or not the applicant's name is in the list of names of those who passed
    unambiguous_df = merged_df[~merged_df['names'].isin(passing_candidates)]

    # Creates a new dataframe for each of the passing candidates and adds it to the final dataframe
    combined_df = []
    for name in passing_candidates:
        name_df = merged_df[merged_df['names'] == name]
        if len(name_df) > 1:
            print(name_df)
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
            unambiguous_df.append(pd.merge(name_df, name_scores, how='outer', left_on='names', right_on='names'))
            combined_df.append(pd.merge(name_df, name_scores, how='outer', left_on='names', right_on='names'))
    print(unambiguous_df.drop(columns='names'))
    return unambiguous_df.drop(columns='names')


def all_merges(df1, df2, df3, df4):
    merge1 = first_merge(df1, df2)
    merge2 = second_merge(merge1, df3)
    final_df = third_merge(merge2, df4)
    return final_df

    # # Creates a dictionary for each column where the value is a list of all column enties in the merged dataframe
    # merged_df_dict = {'join_col': []}
    # for column in merged_df.columns:
    #     merged_df_dict[column] = []
    #     for entry in merged_df.to_dict()[column]:
    #         merged_df_dict[column].append(merged_df.to_dict()[column][entry])
    #
    # # Creates a dictionary of with values that correspond to rows in the new dataframe
    # new_df_dict = {'join_col2': {'name': [], 'start_date': ''}}
    # for column in new_df.columns:
    #     new_df_dict[column] = []
    #     for entry in new_df.to_dict()[column]:
    #         new_df_dict[column].append(merged_df.to_dict()[column][entry])
    #     if column in ['first_name', 'last_name']:
    #         new_df_dict['join_col2'].append()
    #
    #
    #
    # final_df_template = []
    # for row_number in range(0, len(merged_df_as_dict['first_name'])):
    #     if merged_df_as_dict['first_name'][row_number] == new_df_as_dict['first_name'][row_number] and \
    #        merged_df_as_dict['last_name'][row_number] == new_df_as_dict['last_name'][row_number] and \
    #        merged_df_as_dict['date'] < new_df_as_dict['start_date'] and merged_df_as_dict['result']:
    #         final_df_template.append()
    #
    # # Join the 2 dataframes on the index provided
    # new_df.join(merged_df.set_index('names'), on='names')
    # return new_df.drop(['names'], axis=1)


# charlotte_dict = {...}
# katie_dict = {...}

#df1 = pd.DataFrame([charlotte_dict, katie_dict])