# Sapir Avrahami
# 27.8.2020

import json
import pandas as pd

# gets the pandas dataframe, cleans it up (i.e. set correct indexes),
# return the modified dataframe.
def df_cleanup(df):
    index = df.head(1).combine_first(df.head(2)).T
    df.columns = index

    df = df.iloc[2:]
    df['bodyparts', 'coords'].astype(int)
    df = df.set_index(df['bodyparts', 'coords'])
    df = df.drop(df.columns[0], axis=1)
    df = df.astype('float')
    return df

# get the given json, breaks it up into dictionary:
# <key, value> = <'frame_index', corresponding json part>
# the key is the 'frame_index' because they location of each json part can be random.
# returns the dictionary
def json_to_dict(aeden_json):
    jdict = {}

    for index in aeden_json['frame_annotations']:
        id= aeden_json['frame_annotations'][index]['frame_index'];
        jdict.update({id: aeden_json['frame_annotations'][index]})
    return jdict

# this method is used by dp.apply() to create a 'keypoints' json row in the dataframe.
# this will be merged later into the final json.
# returns the keypoints json
def get_keypoints_json(row):
    jkp= {
        "head": {
            "x1": row[0],
            "y1": row[1],
            "rate": row[2]
        },
        "nose": {
            "x1": row[3],
            "y1": row[4],
            "rate": row[5]
        },
        "coccyx": {
            "x1": row[6],
            "y1": row[7],
            "rate": row[8]
        },
        "tail": {
            "x1": row[9],
            "y1": row[10],
            "rate": row[11]
        },
    }
    return jkp;

# merges the information from the correct row in the dataframe with the corresponding
# json from the json dictionary.
# returns the formulated row.
def merge_data(df_row, json_line):
    new_json = {}
    new_json['frame_index'] = json_line['frame_index']
    new_json['objects'] = []
    new_json['objects'].append({
        'attributes': {},
        'category': json_line['dogs'][0]['category'],
        'children': json_line['dogs'][0]['children'],
        'coordinates': {
            'x1': json_line['dogs'][0]['x1'],
            'x2': json_line['dogs'][0]['x2'],
            'y1': json_line['dogs'][0]['y1'],
            'y2': json_line['dogs'][0]['y2']},
        'id': 0,
        'keypoints': df_row,  # need to get it form dp
        'rate': json_line['dogs'][0]['rate']

    })

    r = json.dumps(new_json)
    loader_r = json.loads(r)
    return loader_r

# like merge_data(), with the difference where json dictionary value does not exist.
def insert_data(index, df_row):

    new_json = {}
    new_json['frame_index'] = index
    new_json['objects'] = []
    new_json['objects'].append({
        'attributes': {},
        'category': None,
        'children': None,
        'coordinates': {
            'x1': None,
            'x2': None,
            'y1': None,
            'y2': None
        },
        'id': 0,
        'keypoints': df_row,
        'rate': None
    })

    r = json.dumps(new_json)
    loader_r = json.loads(r)
    return loader_r

# get pandas dataframe and json dictionary,
# The driver function that forms the desired json.
# returns the final json
def create_json(df, json_dict):
    new_json = {}
    new_json['existed_task'] = None
    new_json['video_name'] = "Aeden_session_1_trial_1.mp4"
    new_json['fps'] = 29
    new_json['width'] = 1280
    new_json['height'] = 720
    new_json['frame_annotations'] = {}

    df['keypoints'] = df.apply(get_keypoints_json, axis=1)

    for ind, row in df.iterrows():
        if (int(ind)) in json_dict.keys():
            new_json['frame_annotations'].update({
                ind: merge_data(row['keypoints'], json_dict[int(ind)])
                })
        else:
            new_json['frame_annotations'].update({
                ind: insert_data(ind, row['keypoints'])
            })
    return new_json

# main function, reads in the original csv and json,
# calls all necessary methods and saves the new
# created json as result.json
if __name__ == '__main__':
    aeden_pd=pd.read_csv("Aeden_session_1_trial_1.csv")

    with open('Aeden_session_1_trial_1.json') as jf:
        aeden_json= json.load(jf)

    aeden_pd = df_cleanup(aeden_pd)
    json_dict= json_to_dict(aeden_json)

    new_json= create_json(aeden_pd, json_dict)

    with open('result.json', 'w') as ofile:
        json.dump(new_json, ofile, indent=4)