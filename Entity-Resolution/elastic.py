from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import scan

from ER import abbreviationsCheck


client = Elasticsearch(
    cloud_id="5a253761e0f2466baedd513681b7723e:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQwY2ZkZDVjZDNmZGQ0NzNjYmJiZjYzNzdkYjE3YTI1NyRkOWNlY2IwMDAyM2M0NGJjYWUzYWY2NjEyODczMThjNQ==", 
    api_key="NklNR0xKQUJ6VWRlaTd2RWgycTA6T1dQR0lnTjlSSHlMelRzNl9FNDVoQQ==",
    timeout=30,
    retry_on_timeout=True,
    max_retries=5
)


def resolve(unresolved_entity, best_match, index_name):
    if best_match is None:  # Insert unresolved entity as a new entity in the resolved_entities index
        unresolved_entity['aliases'] = []
        response = client.index(
            index=index_name,
            body=unresolved_entity
        )
        print(f"Inserted entity {unresolved_entity['Name']} into {index_name}")

    else:  # Add unresolved entity as an alias to the best match
        aliases = best_match['_source']['aliases']
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
        print(f"Added alias {unresolved_entity['Name']} to entity {best_match['_source']['Name']} in {index_name}")


# resolve({'Name': 'Thulasi G', 'ID': '197861', 'title': 'POL', 'resolved': False}, 
#         {'_index': 'new_resolved_entities_index', '_id': 'soMWPpABzUdei7vE05IS', '_score': 1.0, '_source': {'Name': 'Thulasi G', '
# ID': '197861', 'title': 'POL', 'resolved': False}} )

def extract_entities(index_name, limit=None):
    if not client.indices.exists(index=index_name):
        print(f"Index '{index_name}' does not exist.")
        return False

    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "title": "POL"
                    }
                }
            }
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
    page = client.search(index=index_name, body=query, scroll='2m', size=1000)
    scroll_id = page['_scroll_id']
    hits = page['hits']['hits']
    
    while len(hits) > 0:
        entities.extend(hits)
        page = client.scroll(scroll_id=scroll_id, scroll='2m')
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

    return entities
 
