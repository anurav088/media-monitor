import csv
import json
from calais_extractor import calais_call


def pipeline(input_file, output_file, batch_size, total):
    articles = []
    try:
        with open(input_file, 'r', encoding='ISO-8859-1') as csvfile:

            reader = csv.DictReader(csvfile)
            article_count = 0
            batch = []
            batch_count = 0

            for row in reader:
                
                    article_text = row['Text']
                    batch.append(article_text)
                    batch_count += 1
                    
                    if batch_count == batch_size:
                      
                      batch_count = 0
                      string_to_pass = ''
                      article_lengths = []

                      for i in batch:  
                        article_structure = {i: {}}
                        articles.append(article_structure)
                        article_lengths.append(len(i))
                        string_to_pass += i + '\n\n'

                      entities = calais_call(string_to_pass)
                      if entities:
                        for i in entities:
                            
                                offset = entities[i]['offset'][0]

                                if offset == 0:
                                    counter = 1

                                else: 
                                    position = 0
                                    counter = 0
                                    
                                    
                                    while position < offset:
                                        position += (article_lengths[counter]+2)
                                        counter += 1
                                    
                                # article = batch[counter-1]
                                index = article_count + counter - 1
                                articles[index][batch[counter - 1]][i] = entities[i]['detections']
                                                                   
           
                      batch = []
                      article_count += batch_size
                      print(f'processed {article_count}')

                    
                    if article_count >= total:
                        break

    except Exception as e:
        print(f"Error: {e}")
        pass        

    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(articles, jsonfile, ensure_ascii=False, indent=4)

# Example usage
input_file = r"C:\Users\Anurav\Research\NER\FinalOutputWithText.csv"
output_file = r"C:\Users\Anurav\Research\NER\articles_entities.json"
batch_size = 14
total = 7000

pipeline(input_file, output_file, batch_size, total)

'''
batch-send n articles at a time to calais
make each article a separate key in the dictionary
map entities to the key based on off-set values
'''
