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

def writeJSONdata(merged_dict):

    ''' File format

    {
      "name": "Log/MAC",
      "description": "",
      "regexTarget": "",
      "examples": [
        {
        "string": "Jan 12 06:26:19: ACCEPT service http from 119.63.193.196 to firewall(pub-nic), prefix: \"none\" (in: eth0 119.63.193.196(5c:0a:5b:63:4a:82):4399 -> 140.105.63.164(50:06:04:92:53:44):80 TCP flags: ****S* len:60 ttl:32)",
        "match": [
            { "start": 119, "end": 136 },
            { "start": 161, "end": 178 }
        ],
        "unmatch": [
            {"start": 0,"end": 119},
            {"start": 136,"end": 161},
            {"start": 178,"end": 215}
        ]
        },
      ]
    }


    '''

    import json

    DIR_DATA = '../data-products/'
    FILENAME_BGS = 'bgs_costing-job_numbers_training-set.json'
    FILENAME_JOB_NO = 'jobstatus-job_numbers_training-set.json'

    for data_name in merged_dict:
        df = merged_dict[data_name]
        if 'bgs' in data_name:
            filename = DIR_DATA + FILENAME_BGS
        else:
            filename = DIR_DATA + FILENAME_JOB_NO

        json_dict = {'name': data_name,
                     }
        example_string = ''
        match = []
        unmatch = []
        pos = 0
        #for i in xrange(len(df)):
        for i in xrange(10):
            # grab the data from the DataFrame
            string = df.iloc[[i]]['string'].values[0]
            valid = df.iloc[[i]]['valid'].values[0]

            # add the new string to the single example
            example_string += string

            # add the start and end position of the flagged string
            flag = {'start': pos, 'end': pos + len(string) - 1}
            if valid:
                match.append(flag)
            elif not valid:
                unmatch.append(flag)

            print flag, len(example_string)

            # move position to next string
            pos += len(string)


        # gather the data
        examples = [{'string': example_string,
                    'match': match,
                    'unmatch': unmatch,
                    },
                    ]
        json_dict['examples'] = examples

        # write the data
        json.dump(json_dict, open(filename, 'w'), indent=4)

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
        n_strings = len(data) * 0.1
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

    # write the data as a csv
    writeData(merged_dict)

    # write the data as an annotated JSON
    writeJSONdata(merged_dict)



if __name__ == '__main__':
    main()

