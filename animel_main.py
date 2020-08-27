import json
import pandas as pd

def get_info_form_json(json_line):
    #print(json_line)

    new_json= {}
    new_json['frame_index']= json_line['frame_index']
    new_json['objects']= []
    new_json['objects'].append({
        'attributes': {},
        'category': json_line['dogs'][0]['category'],
        'children': json_line['dogs'][0]['children'],
        'coordinates': {
            'x1': json_line['dogs'][0]['x1'],
            'x2': json_line['dogs'][0]['x2'],
            'y1': json_line['dogs'][0]['y1'],
            'y2': json_line['dogs'][0]['y2']},
        'id': json_line['dogs'][0]['id'],
        'keypoints': {},      #need to get it form dp
        'rate': json_line['dogs'][0]['rate']

    })
    #print(new_json)
    #print(aeden_json['frame_annotations'])
    #print("hi!!!")
    r= json.dumps(new_json)
    loader_r= json.loads(r)
    return loader_r

def json_to_dict(aeden_json):
    jdict = {}

    for index in aeden_json['frame_annotations']:
        id= aeden_json['frame_annotations'][index]['frame_index'];
        jdict.update({id: aeden_json['frame_annotations'][index]})
    return jdict

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
        "Tail": {
            "x1": row[9],
            "y1": row[10],
            "rate": row[11]
        },
    }
    return jkp;

if __name__ == '__main__':
    aeden_pd=pd.read_csv("Aeden_session_1_trial_1.csv")

    index= aeden_pd.head(1).combine_first(aeden_pd.head(2)).T
    #print(index)
    aeden_pd.columns= index
    #aeden_pd.rename_axis('data').reset_index()

    #aeden_pd.columns=(aeden_pd.iloc[0], aeden_pd.iloc[1])
    aeden_pd= aeden_pd.iloc[2:]
    aeden_pd['bodyparts', 'coords'] = aeden_pd['bodyparts', 'coords'].astype(int)
    aeden_pd= aeden_pd.set_index(aeden_pd['bodyparts', 'coords'])
    aeden_pd = aeden_pd.drop(aeden_pd.columns[0], axis=1)
    #aeden_pd= aeden_pd.drop(('bodyparts', 'coords'), axis = 1, inplace = True)

    with open('Aeden_session_1_trial_1.json') as jf:
        aeden_json= json.load(jf)

    print(aeden_pd)
    #print(aeden_pd['bodyparts', 'coords'])
    print(aeden_pd.loc[0])
    json_dict= json_to_dict(aeden_json)
    print(json_dict)

    new_json= {}
    new_json['existed_task']=[]
    new_json['video_name'] = "Aeden_session_1_trial_1.mp4"
    new_json['fps'] = 29
    new_json['width'] = 1280
    new_json['height'] = 720
    new_json['frame_annotations']= {}

    aeden_pd['keypoints']= aeden_pd.apply(get_keypoints_json, axis=1)
    aeden_pd.to_csv('trying.csv')


    #for index in json_dict:
        #print(json_dict[index])

        #new_json['frame_annotations'].update({
        #    index: get_info_form_json(aeden_json['frame_annotations'][index])
        #})

        #new_json['frame_annotations'].append({
        #    index: get_info_form_json(aeden_json['frame_annotations'][index])
        #})

    print(new_json)
    #new_json['frame_annotations'].append()

    with open('data1.json', 'w') as ofile:
        json.dump(new_json, ofile)
    data = {}
    data['people'] = []
    data['people'].append({
        'name': 'Scott',
        'website': 'stackabuse.com',
        'from': 'Nebraska'
    })
    data['people'].append({
        'name': 'Larry',
        'website': 'google.com',
        'from': 'Michigan'
    })
    data['people'].append({
        'name': 'Tim',
        'website': 'apple.com',
        'from': 'Alabama'
    })

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)