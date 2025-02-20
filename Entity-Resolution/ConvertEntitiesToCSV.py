import csv
from elasticsearch import Elasticsearch, helpers

client = Elasticsearch(
    cloud_id="ES_CLOUD_ID", 
    api_key="ES_API_KEY",
    timeout=30,
    retry_on_timeout=True,
    max_retries=5
)

def fetch_all_documents(index_name):
    query = {
        "size": 10000,  
        "query": {
            "nested": {
                "path": "aliases",
                "query": {
                    "bool": {
                        "must": [
                            {
                                "exists": {
                                    "field": "aliases.ID"
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
    response = client.search(index=index_name, body=query, scroll='2m')
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    
    all_documents = hits
    
    while len(hits) > 0:
        response = client.scroll(scroll_id=scroll_id, scroll='2m')
        hits = response['hits']['hits']
        all_documents.extend(hits)
    
    return all_documents

def process_documents(documents):
    rows = []
    for doc in documents:
        source = doc['_source']
        entity = f"{source['Name']}({source['title']},{source['ID']})"
        
        aliases = source.get('aliases', [])
        sorted_aliases = sorted(aliases, key=lambda x: x['confidence'], reverse=True)
        aliases_str = ", ".join([f"{alias['Name']}({alias['title']},{alias['ID']},{alias['confidence']})" for alias in sorted_aliases])
        
        rows.append([entity, aliases_str])
    
    return rows

def save_to_csv(rows1, filename):
    header = ['Entities', 'Aliases']
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows1)
