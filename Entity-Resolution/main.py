'''full pipeline
1. iterate through unresolved entities and return entities | input: None, output: dictionary / list of dicts 
2. run algo 1, get a list of dicts (top-10 matches) | input: str (name), output: list of dicts 
3. run algo 2, determine best match | input: str (name), list of dicts (top-10), output: dictionary 
4. merger | input: dictionary (unresolved_entity), dictionary (best-match), output: None'''

from ER import *
from elastic import *

def pipeline(limit = None):
    
    unresolved_entities_index = 'unresolved_entities'
    resolved_entities_index = 'resolved_entities'
    
    entities_to_process = extract_entities(index_name=unresolved_entities_index, limit = limit)

    for en in entities_to_process:
        print(en)
        _name = name(en)
        _top_ten_entities = top_ten_entities(_name, index_name=resolved_entities_index)
        _best_match = best_match(_name, _top_ten_entities)
        resolve(en['_source'], _best_match, index_name = resolved_entities_index)


pipeline(1000)
        


