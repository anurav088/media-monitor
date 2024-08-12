import pandas as pd
import os
import re
import gensim
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import gensim.corpora as corpora
import pyLDAvis.gensim_models as gensimvis
import pickle
import pyLDAvis
from pprint import pprint 

# Download stopwords
nltk.download('stopwords')

# Initialize stop words
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'due', 'said', 'could', 'get', 'would'])

# Function to preprocess sentences into words
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

# Function to remove stopwords
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def main():
    # Load your dataw
    df = pd.read_csv(r"C:\Users\Tanisha Iyer\Desktop\corporate competition NEW\2023_final_output.csv")

    # Select and preprocess a sample of the data
    papers = df.drop(columns=['Title', 'Date'], axis=1).sample(50)
    papers['Text_processed'] = papers['Text'].map(lambda x: re.sub('[,\.!?]', '', x)).map(lambda x: x.lower())

    #  Generate a word cloud - (optional)
    #  long_string = ','.join(list(papers['Text_processed'].values))
    #  wordcloud = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color='steelblue')
    #  wordcloud.generate(long_string)
    #  wordcloud.to_image()

    # Further text preprocessing
    data = papers.Text_processed.values.tolist()
    data_words = list(sent_to_words(data))
    data_words = remove_stopwords(data_words)

    # Create a dictionary and corpus
    id2word = corpora.Dictionary(data_words)
    corpus = [id2word.doc2bow(text) for text in data_words]

    # Train the LDA model
    num_topics = 10
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics=num_topics)

    # Print the topics discovered by LDA
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    # Define file paths
    results_dir = r"C:\Users\Tanisha Iyer\Desktop\results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    LDAvis_data_filepath = os.path.join(results_dir, 'ldavis_prepared_' + str(num_topics))

    # Serialize the LDA visualization object and save it as a binary file
    LDAvis_prepared = gensimvis.prepare(lda_model, corpus, id2word)
    with open(LDAvis_data_filepath, 'wb') as f:
        pickle.dump(LDAvis_prepared, f)

    # Load the LDA visualization object from the binary file
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)

    # Save the LDA visualization as an HTML file
    pyLDAvis.save_html(LDAvis_prepared, os.path.join(results_dir, 'ldavis_prepared_' + str(num_topics) + '.html'))

    return LDAvis_prepared

if __name__ == "__main__":
    main()
