from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan

from ER import abbreviationsCheck, name


client = Elasticsearch(
    cloud_id="ES_CLOUD_ID", 
    api_key="ES_API_KEY",
    timeout=30,
    retry_on_timeout=True,
    max_retries=5
)


def resolve(unresolved_entity, best_match, index_name):
    unresolved_entity['Name'] = unresolved_entity['Name'].upper()
    
    if best_match is None:  # Insert unresolved entity as a new entity in the resolved_entities index
        unresolved_entity['aliases'] = []
        response = client.index(
            index=index_name,
            body=unresolved_entity
        )
        print(f"Inserted entity {unresolved_entity['Name']} into {index_name}")

    else:  # Add unresolved entity as an alias to the best match
        
        aliases = best_match['_source']['aliases']
        
        if len(unresolved_entity['Name']) <= len(name(best_match)):
            alias_entry = {
                'ID': unresolved_entity['ID'],
                'title': unresolved_entity['title'],
                'Name': unresolved_entity['Name'],
                'confidence': best_match['confidence']  
            }
            aliases.append(alias_entry)
                
            update_body = {
                "doc": {
                    "aliases": aliases
                }
            }
            response = client.update(
                index=index_name,
                id=best_match['_id'],
                body=update_body
            )
        else:
    
            alias_entry = {
                'ID': best_match['_source']['ID'],
                'title': best_match['_source']['title'],
                'Name': best_match['_source']['Name'],
                'confidence': best_match['confidence']  
            }

            aliases.append(alias_entry)
                
            update_body = {
                "doc": {
                    "Name": unresolved_entity['Name'],
                    "ID": unresolved_entity['ID'],
                    "title": unresolved_entity['title'],
                    "aliases": aliases
                }
            }
            response = client.update(
                index=index_name,
                id=best_match['_id'],
                body=update_body
            )
        print(f"Added alias {unresolved_entity['Name']} to entity {best_match['_source']['Name']} in {index_name}")
    


def extract_entities(index_name, limit=None):
    if not client.indices.exists(index=index_name):
        print(f"Index '{index_name}' does not exist.")
        return []

    query = {
        "query": {
            "match_all": {}
        },
        "sort": [
            {
                "ID": {
                    "order": "asc"
                }
            }
        ]
    }

    entities = []
    batch_size = 10000
    current_size = limit if limit and limit < batch_size else batch_size
    page = client.search(index=index_name, body=query, scroll='2m', size=current_size)
    scroll_id = page['_scroll_id']
    hits = page['hits']['hits']
    
    while len(hits) > 0:
        entities.extend(hits)
        if limit and len(entities) >= limit:
            break
        page = client.scroll(scroll_id=scroll_id, scroll='2m')
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

    return entities[:limit] if limit else entities
