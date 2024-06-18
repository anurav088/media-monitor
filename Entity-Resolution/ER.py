from metaphone import doublemetaphone
from Levenshtein import distance as levenshtein_distance


def fuzzyCheck(a,b):
    if a == b:
        return True
    elif doublemetaphone(a) == doublemetaphone(b):
        return True
    elif (a[0] == b[0]): 
        if (len(a) <= 6) and (levenshtein_distance(a,b) == 1):
            return True
        elif (len(a) > 6) and (levenshtein_distance(a,b) == 2):
            return True

def exactMathPer(name1, name2):

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
        if len(i) > 1:
            for j in wordList2:
                if len(j)>1 and fuzzyCheck(i,j): 
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


def score(unresolved_entity, current_entity): 
    ''' pass unresolved and current entities as inputs and return relevancy score from
        an ElasticSearch query
        To be written
        ''' 
    return 
    

# algo 2 
def best_match(unresolved_entity, top_ten_entities):
    best_match = None
    for i in top_ten_entities:
        if (fuzzyMatchPer(unresolved_entity, i) and score(unresolved_entity, i) > 10) or exactMathPer(unresolved_entity, i):
            best_match = i
            break
    return best_match


