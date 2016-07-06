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

        n_strings = len(data)
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

def main():

    ''' Runs main function.

    '''

    # get the data as a dict of pandas DataFrame objects
    data_dict = loadData()

    # generate fake data
    data_dict = addFakeData(data_dict)

    #print data_dict['fake']['bgs']

    data = data_dict['fake']['job']['string'].values
    matches = lm.getRegexMatches(data,
                                 r'\d{6}',
                                 )

    print len(data)
    print np.sum(matches)


if __name__ == '__main__':
    main()

