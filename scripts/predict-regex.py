#!/usr/bin/python

# import external modules
import numpy as np
import pandas as pd
import localmodule as lm

def loadData():

    DIR_DATA = '../data/'
    FILENAME_BGS = 'bgs_costing-job_numbers.csv'
    FILENAME_JOB_NO = 'jobstatus-job_numbers.csv'

    data_bgs = pd.read_csv(DIR_DATA + FILENAME_BGS,
                           sep=',',
                           header=0,
                           index_col=False,
                           names=('string',),
                           )

    data_job = pd.read_csv(DIR_DATA + FILENAME_JOB_NO,
                           sep=',',
                           header=0,
                           index_col=False,
                           names=('string',),
                           )

    return {'data': {'bgs': data_bgs, 'job': data_job}}

def writeData(merged_dict):

    DIR_DATA = '../data-products/'
    FILENAME_BGS = 'bgs_costing-job_numbers_training-set.csv'
    FILENAME_JOB_NO = 'jobstatus-job_numbers_training-set.csv'

    for data_name in merged_dict:
        df = merged_dict[data_name]
        if 'bgs' in data_name:
            filename = FILENAME_BGS
        else:
            filename = FILENAME_JOB_NO

        df.to_csv(DIR_DATA + filename,
                  index=False,
                  header=True,
                  )

def addFakeData(data_dict):

    import localmodule as lm

    data_dict['fake'] = {}
    string_length = 6

    for df_name in data_dict['data']:
        df = data_dict['data'][df_name]
        data = df['string'].values

        data_string = ''
        for element in data:
            data_string += str(element)

        # Number of strings to randomly generate
        n_strings = len(data) * 10
        n_strings = int(n_strings)

        unique_characters = ''.join(set(data_string))
        #unique_characters = np.unique(data_string)

        # get the frequency
        character_probabilities = np.empty(len(unique_characters))

        for i, char in enumerate(unique_characters):
            character_probabilities[i] = data_string.count(char)

        # generate fake strings
        fake = lm.generateRandomStringList(\
                   n_strings=n_strings,
                   string_length=string_length,
                   character_choices=unique_characters,
                   character_probabilities=character_probabilities,
                   )

        #print fake

        # turn list into dataframe
        df_fake = pd.DataFrame(fake, columns=['string'])

        # add fake dataframe to data dictionary
        data_dict['fake'][df_name] = df_fake

    return data_dict

def mergeDatasets(data_dict):

    # Add valid = yes for data and valid = no for fakes
    for df_name in data_dict['data']:
        df = data_dict['data'][df_name]
        df['valid'] = pd.Series(1, df.index)
    for df_name in data_dict['fake']:
        df = data_dict['fake'][df_name]
        df['valid'] = pd.Series(0, df.index)


    # merge dfs
    merged_dict = {}
    for dataset_name in data_dict['data']:
        df_data = data_dict['data'][dataset_name]
        df_fake = data_dict['fake'][dataset_name]

        df_merged = pd.concat([df_data, df_fake])
        merged_dict[dataset_name] = df_merged

    return merged_dict

def main():

    ''' Runs main function.

    '''

    # get the data as a dict of pandas DataFrame objects
    data_dict = loadData()

    # generate fake data
    data_dict = addFakeData(data_dict)

    #print data_dict['fake']['bgs']

    data = data_dict['fake']['job']['string'].values

    # merge datasets to have valid and invalid input
    merged_dict = mergeDatasets(data_dict)

    writeData(merged_dict)



if __name__ == '__main__':
    main()

