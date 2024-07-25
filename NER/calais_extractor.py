import requests 


def extract_names(data):
    names = {}
    
    for i in data:
        if 'name' in data[i]:
            names[(data[i]['name'])] = {"detections":[], "offset":[]}
            for j in data[i]['instances']:
                names[(data[i]['name'])]["detections"].append({j['exact']: j['detection']})
                names[(data[i]['name'])]["offset"].append(j['offset'])

 
    return names

def calais_call(body):

    url = 'https://api-eit.refinitiv.com/permid/calais'
   
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
        'Content-Type': 'text/raw',
        'x-ag-access-token': 'umsyYonUf1c03lenJzrpSH9Uu04Hl1Tf', 
        'x-calais-selectiveTags': 'topic-selfservice,company,person,organization,city,region',
        'outputFormat': 'application/json',
        'omitOutputtingOriginalText': 'true',
        'x-calais-content-class': 'news',
    }

    response = requests.post(url, data=body, headers=headers)


    if response.status_code == 200:

        data = response.json()
        names = extract_names(data)
        return names 
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

