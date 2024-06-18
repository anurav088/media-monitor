<h1>Media Monitor</h1>
The project is guided by Professor Anirban Sen and is aimed at creating a tool that tracks the evolution of mass media in India via natural language processing (NLP) analysis over time. 

<h2>File Descriptions</h2>
<ul>
  <li>
    <u> preprocessing.ipynb </u>: contains code to pre-process the article text and generate the file preprocessed_TOI_FarmersProtests.csv
  </li> <br>
  <li>
    <u> word2vec.ipynb </u>: contains code to embed, plot, and compare vectors for the corpus contained in corpus.txt
  </li> <br>
  <li>
    <u> preprocessed_TOI_FarmersProtests.csv </u> contains the article text that the corpus is generated from using (commented) code in word2vec.ipynb
  </li> <br>
  <li>
    <u> corpus.txt </u> (really long) string of whitespace separated words 
  </li> <br>
  <li>
    <u> pre-training-PCA.html </u> interactive scatter-plot representing word vectors before training, features reduced via PCA 
  </li> <br>
  <li> 
    <u> pre-training-tSNE.html </u> interactive scatter-plot representing word vectors before training, features reduced via tSNE 
  </li> <br>
  <li>
    <u> skipgram-PCA.html </u> interactive scatter-plot representing word vectors after Skip-gram training, features reduced via PCA 
  </li> <br>
   <li>
    <u> skipgram-TSNE.html </u> interactive scatter-plot representing word vectors after Skip-gram training, features reduced via tSNE 
  </li> <br>
   <li>
    <u> cbow-PCA.html </u> interactive scatter-plot representing word vectors after CBOW training, features reduced via PCA 
  </li> <br>
  <li>
    <u> cbow-tSNE.html </u> interactive scatter-plot representing word vectors after CBOW training, features reduced via tSNE 
  </li> 
</ul>

<h2>Notes</h2>
<ol list-style-type:disc>
  <li> To use the interactive plots, simply download and launch them using any web-browser. </li> <br>
  <li> The google news vectors referned have not been in included in the repo because size > 1GB, they can be found at https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?resourcekey=0-wjGZdNAUop6WykTtMip30g</li>
</ol>


