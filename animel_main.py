import json
import pandas as pd

def get_info_form_json(json_line):
    print(json_line)

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
    print(new_json)
    #print(aeden_json['frame_annotations'])
    print("hi!!!")
    r= json.dumps(new_json)
    loader_r= json.loads(r)
    return loader_r


if __name__ == '__main__':
    aeden_pd=pd.read_csv("Aeden_session_1_trial_1.csv")
    aeden_pd.columns=aeden_pd.iloc[0]
    aeden_pd.drop(aeden_pd.index[0])
    #aeden_json=pd.read_json('Aeden_session_1_trial_1.json')

    with open('Aeden_session_1_trial_1.json') as jf:
        aeden_json= json.load(jf)

    #print(aeden_pd)
    #print(aeden_json)

    #print(aeden_pd.loc[1])
    #print(aeden_pd.loc[2])
    #print(aeden_json)

    new_json= {}
    new_json['existed_task']=[]
    new_json['video_name'] = "Aeden_session_1_trial_1.mp4"
    new_json['fps'] = 29
    new_json['width'] = 1280
    new_json['height'] = 720
    new_json['frame_annotations']= {}

    for index in aeden_json['frame_annotations']:
        new_json['frame_annotations'].update({
            index: get_info_form_json(aeden_json['frame_annotations'][index])
        })

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