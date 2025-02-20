from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch(
cloud_id="ES_CLOUD_ID",
api_key="ES_API_KEY")


# Create index with mapping
# index_name = 'unresolved'
# mapping = {
#     "mappings": {
#         "properties": {
#             "Name": {"type": "text"},
#             "ID": {"type": "keyword"},
#             "title": {"type": "keyword"}
#         }
#     }
# }

# # Delete the index if it exists
# if es.indices.exists(index=index_name):
#     es.indices.delete(index=index_name)

# # Create the index
# es.indices.create(index=index_name, body=mapping)

def index_csv_data(file_path, title):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        actions = []
        for row in reader:
            action = {
                "_index": 'res_conf2',
                "_source": {
                    "Name": row['Name'],
                    "ID": row['ID'],
                    "title": title,
                    "aliases": []
                }
            }
            actions.append(action)
        helpers.bulk(es, actions)

