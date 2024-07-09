import requests 
import json
file_path="sample_article_1.json"


url="https://api-eit.refinitiv.com/permid/calais"

headers={
"Content-Type": "text/xml",
"outputFormat": "application/json",
"x-ag-access-token" : "bhZBI6b0lHII7EbgVXumimL2DSZUBdx5",
"x-calais-selectiveTags" :"topic-selfservice,company,person,city"

}
try:
    data= "BATHINDA: Punjab jails minister Sukhjinder Singh Randhawa has ordered an investigation into the December 30 assault on a farmer union’s vice-president in Faridkot jail. Randhawa said he had asked ADGP (jails) to find how a gangster and his henchmen beat up the inmate, Kirti Kisan Union vice president Rajinder Singh. An officer of the rank of deputy inspector general of police (DIG) has been asked to inquire into the matter and fix responsibility of the jail staff. Speaking to TOI, Randhawa said, “I had taken up the matter with ADGP (jails) and asked him to get the matter probed. The ADGP has deputed a DIG-level officer to investigate by concentrating on talking to the inmate who was beaten up and those who were around. We will reach to the bottom of the matter and anyone found guilty of dereliction of duty will be taken to task.” Rajinder was attacked in the jail on December 30 evening. With blunt injuries on the body, he was admitted to Guru Gobind Singh Medical College, Faridkot. Nishan Singh, who is serving a life sentence for abducting and raping a minor girl, is behind the attack. A case has been registered against Nishan and 17 others. Farmer organisation activists KKU presid "
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    print(response.status_code)
    json_object=response.json()
    with open("/Users/anandagarwal/Media Graph NER/sample_article_4.json", "w") as fout:
        json.dump(json_object, fout, indent=4)
except requests.exceptions.RequestException as e:
    print(f"HTTP Request failed: {e}")