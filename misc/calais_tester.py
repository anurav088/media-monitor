import requests 

body = 'BATHINDA: Punjab jails minister Sukhjinder Singh Randhawa has ordered an investigation into the December 30 assault on a farmer union‚Äôs vice-president in Faridkot jail. Randhawa said he had asked ADGP (jails) to find how a gangster and his henchmen beat up the inmate, Kirti Kisan Union vice president Rajinder Singh. An officer of the rank of deputy inspector general of police (DIG) has been asked to inquire into the matter and fix responsibility of the jail staff. Speaking to TOI, Randhawa said, ‚ÄúI had taken up the matter with ADGP (jails) and asked him to get the matter probed. The ADGP has deputed a DIG-level officer to investigate by concentrating on talking to the inmate who was beaten up and those who were around. We will reach to the bottom of the matter and anyone found guilty of dereliction of duty will be taken to task.‚Äù Rajinder was attacked in the jail on December 30 evening. With blunt injuries on the body, he was admitted to Guru Gobind Singh Medical College, Faridkot. Nishan Singh, who is serving a life sentence for abducting and raping a minor girl, is behind the attack. A case has been registered against Nishan and 17 others. Farmer organisation activists KKU presid'

url="https://api-eit.refinitiv.com/permid/calais"

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

def extract_names(data):
    names = {}
    
    for i in data:
        if 'name' in data[i]:
            names[(data[i]['name'])] = []
            for j in data[i]['instances']:
                names[(data[i]['name'])].append({j['exact']: j['detection']})
 
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



print(calais_call(body))
