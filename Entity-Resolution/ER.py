import time 

from metaphone import doublemetaphone
from Levenshtein import distance as levenshtein_distance
from elasticsearch import Elasticsearch
from collections import Counter

client = Elasticsearch(
    cloud_id="5a253761e0f2466baedd513681b7723e:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQwY2ZkZDVjZDNmZGQ0NzNjYmJiZjYzNzdkYjE3YTI1NyRkOWNlY2IwMDAyM2M0NGJjYWUzYWY2NjEyODczMThjNQ==", 
    api_key="NklNR0xKQUJ6VWRlaTd2RWgycTA6T1dQR0lnTjlSSHlMelRzNl9FNDVoQQ==",
    timeout=30,
    retry_on_timeout=True,
    max_retries=5)


def name(entity):
    return entity["_source"]["Name"]

def abbreviationsCheck(name1, name2):
    
    initials1 = [word[0].upper() for word in name1.split()]
    initials2 = [word[0].upper() for word in name2.split()]

    initials1.sort(), initials2.sort()

    counter1, counter2 = Counter(initials1), Counter(initials2)
    intersection = list((counter1 & counter2).elements())
    
    return (intersection == initials1) or (intersection == initials2) 
            


def fuzzyCheck(a,b):
    if a == b:
        return True
    elif doublemetaphone(a) == doublemetaphone(b):
        return True
    elif (a[0] == b[0]): 
        if (len(a) <= 6) and (levenshtein_distance(a,b) <= 1):
            return True
        elif (len(a) > 6) and (levenshtein_distance(a,b) <= 2):
            return True
    return False 

def exactMatchPer(name1, name2):

    name1, name2 = name1.lower(), name2.lower()
    wordList1 = name1.split()
    wordList2 = name2.split()
    if wordList1 == wordList2:
        return True
    

def fuzzyMatchPer(name1, name2):
    
    name1, name2 = name1.lower(), name2.lower()
    wordList1, wordList2 = name1.split(), name2.split()
    
    #step 1 : remove matching initials 
    while (len(wordList1[0]) == len(wordList2[0]) == 1) and (wordList1[0] == wordList2[0]):
        wordList1.pop(0)
        wordList2.pop(0)
    
    #step 2 : remove similar multi-letter words
    similar = set()

    for i in wordList1:
        for j in wordList2:
            if fuzzyCheck(i,j): 
                    similar.add(i)
                    similar.add(j)
   
    wordList1 = [i for i in wordList1 if i not in similar]
    wordList2 = [j for j in wordList2 if j not in similar]

    #step 3 : remove initial-word pairs 
    if len(wordList1) != len(wordList2):
        return False 
    
    similar = set()

    for i in wordList1:
        if len(i) == 1: #check for initials from list1 mapping to words in list2
            for j in wordList2:
                if i == j[0]:
                    similar.add(i)
                    similar.add(j)
        else:
            for j in wordList2:
                if j == i[0]: #check for words in list1 mapping to initials in list2
                    similar.add(i)
                    similar.add(j)

    #updating lists        
    wordList1 = [i for i in wordList1 if i not in similar]
    wordList2 = [j for j in wordList2 if j not in similar]          
    
    #final check/step
    if wordList1 == wordList2:
        return True 
    else:
        return False


# algo 1 
def top_ten_entities(unresolved_entity, index_name):

    # index_name = 'resolved_entities'

    entity_title = unresolved_entity['_source']['title']
    response = client.search(
        index=index_name,
        body={
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "Name": unresolved_entity['_source']['Name']
                        }
                    }
                   
                }
            }
        }
    )
    
    hits = response['hits']['hits']
    scores = [hit['_score'] for hit in hits]
    
    if scores:
        max_score = max(scores)
        min_score = min(scores)
        if (max_score - min_score) != 0:
            normalized_scores = [(score - min_score) / (max_score - min_score) for score in scores]
        else:
            normalized_scores = [score for score in scores]
    else:
        normalized_scores = []
    results = []

    for hit, score in zip(hits, scores):
        result = hit
        result['confidence'] = score
        results.append(result)
      
    return results 

# algo 2 

def best_match(unresolved_entity, top_ten_entities):

    best_match = None
    
    for i in top_ten_entities:
        if abbreviationsCheck(unresolved_entity, name(i)):
            if ((i['confidence'] > 0.1) and fuzzyMatchPer (unresolved_entity, name(i))):
                if i['_source']['aliases'] != []:
                    for j in (i['_source']['aliases']):
                        flag = True
                        if (fuzzyMatchPer(unresolved_entity, j['Name'])):
                            continue 
                        else: #if even 1 alias does not match
                            flag = False
                            break

                    if flag == True:
                        best_match = i     
                        break           
                else:
                    best_match = i
                    break
        else:
            continue 
        
        
    return best_match
