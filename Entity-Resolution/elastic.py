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
    # index_name = 'resolved_entities'
    if best_match == None: # Insert unresolved entity as a new entity in the resolved_entities index
        unresolved_entity['aliases'] = []
        response = client.index(
            index=index_name,
            body=unresolved_entity
        )
        print(f"Inserted entity {unresolved_entity['Name']} into resolved_entities")

    else: # Add unresolved entity as an alias to the best match
        aliases = best_match['_source']['aliases']
        aliases.append({'ID': unresolved_entity['ID'], 'title': unresolved_entity['title'], 'Name': unresolved_entity['Name']})
            
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
        print(f"Added alias {unresolved_entity['Name']} to entity {best_match['_source']['Name']} in resolved_entities")




def extract_entities(index_name, limit = None):
        
        # index_name = 'unresolved_entities'

        if not client.indices.exists(index=index_name):
            print(f"Index '{index_name}' does not exist.")
            return False

        if limit == None: 
            query = {"query": {"match_all": {}}}
        else:
            query = {"query": {"match_all": {}}, "size": limit}

        query["sort"] = [{"ID": {"order": "asc"}}]
    
        response = client.search(index=index_name, body=query)
        docs = response['hits']['hits']
        
        entities = []
        for doc in docs:
             entities.append(doc)
        
        return entities
   
 
