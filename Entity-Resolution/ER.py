import time 

from metaphone import doublemetaphone
from Levenshtein import distance as levenshtein_distance
from elasticsearch import Elasticsearch


client = Elasticsearch(
    cloud_id="5a253761e0f2466baedd513681b7723e:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQwY2ZkZDVjZDNmZGQ0NzNjYmJiZjYzNzdkYjE3YTI1NyRkOWNlY2IwMDAyM2M0NGJjYWUzYWY2NjEyODczMThjNQ==", 
    api_key="NklNR0xKQUJ6VWRlaTd2RWgycTA6T1dQR0lnTjlSSHlMelRzNl9FNDVoQQ==",
    timeout=30,
    retry_on_timeout=True,
    max_retries=5)


def name(entity):
    return entity["_source"]["Name"]

def abbreviationsCheck(name1, name2):
    name1, name2 = name1.lower(), name2.lower()

    wordList1 = name1.split()
    wordList2 = name2.split()

    initials1 = {}
    initials2 = {}

    for i in wordList1:
        if i[0] not in initials1:
            initials1[i[0]] = 1
        else: 
            initials1[i[0]] += 1
            
    for j in wordList2:
        if j[0] not in initials2:
            initials2[j[0]] = 1
        else: 
            initials2[j[0]] += 1
    
    if len(wordList1) <= len(wordList2):
        smaller = initials1
        bigger = initials2
    else:
        smaller = initials2
        bigger = initials1
    
    for i in smaller:
        while smaller[i] > 0:
            if i in bigger and bigger[i] > 0:
                bigger[i] -= 1
                smaller[i] -= 1
            else:
                return False
    return True
            
            


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

    wordList1 = name1.split()
    wordList2 = name2.split()

    #step 1 : remove matching initials 
    while (len(wordList1[0]) == len(wordList2[0]) == 1) and (wordList1[0] == wordList2[0]):
        wordList1 = wordList1[1:]
        wordList2 = wordList2[1:]
    
    #step 2 : remove similar multi-letter words
    wordList1_new = []
    wordList2_new = []
    similar = set()

    for i in wordList1:
        for j in wordList2:
            if fuzzyCheck(i,j): 
                    similar.add(i)
                    similar.add(j)
    #updating lists  
    for i in wordList1:
        if i not in similar:
            wordList1_new.append(i)
    for j in wordList2:
        if j not in similar:
            wordList2_new.append(j)

    wordList1 = wordList1_new
    wordList2 = wordList2_new

    #step 3 : remove initial-word pairs 
    wordList1_new = []
    wordList2_new = []
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
    for i in wordList1:
        if i not in similar:
            wordList1_new.append(i)
    for j in wordList2:
        if j not in similar:
            wordList2_new.append(j)    
    # return wordList1_new, wordList2_new 

    #final check/step
    if wordList1_new == wordList2_new:
        return True 
    else:
        return False


# algo 1 
def top_ten_entities(unresolved_entitiy, index_name):

    # index_name = 'resolved_entities'

    response = client.search(
        index = index_name,
        body = {
            "size": 10,
            "query": {
                "match": {
                    "Name": unresolved_entitiy
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
            normalized_scores = []
    else:
        normalized_scores = []

    results = []

    for hit, score in zip(hits, normalized_scores):
        result = hit
        result['confidence'] = score
        results.append(result)
      
    return results

# algo 2 
'''
1. for this algo, how hard a filter do we want for merging? test for different cases
2. test with main name matching and all / some matching. some = ?'''

def best_match(unresolved_entity, top_ten_entities):

    best_match = None
    
    for i in top_ten_entities:
        if abbreviationsCheck(unresolved_entity, name(i)):
            if ((i['confidence'] > 0.1) and fuzzyMatchPer (unresolved_entity, name(i))):
                if i['_source']['aliases'] != []:
                    for j in (i['_source']['aliases']):
                        flag = True
                        if (fuzzyMatchPer(unresolved_entity, name(j))):
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
    
