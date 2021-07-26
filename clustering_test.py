"""### Import Statements"""

import os
import random
import nltk
import re
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt


"""### Downloading extra dependencies from NLTK"""

# nltk.download('punkt')
# nltk.download('stopwords')


"""### Getting stopwords customized to your problem statement"""

#Use this function to create custom list of stop_words for your Project

# path = r'../Stopwords/stopwords_not_to_be_used.txt' #Add the path to stopwords_not_to_be_used.txt file
# def get_stopwords(path):
#   stopwords = nltk.corpus.stopwords.words('english')
#   not_words = []
#   with open(path,'r', encoding='utf-8') as f:
#     not_words.append(f.readlines())
#   not_words = [word.replace('\n','') for words in not_words for word in words]
#   not_words = set(not_words)
#   stopwords = set(stopwords)
#   customized_stopwords = list(stopwords - not_words)
#   return stopwords,customized_stopwords
#
# stop_words,customized_stopwords = get_stopwords(path)


"""### Loading the Data"""

path = r'./Articles' #Add the path to Articles folder
seed = 137 #Seed value

# def load_data(path,seed):
#   train_texts = []
#   for fname in sorted(os.listdir(path)):
#     if fname.endswith('.txt'):
#       with open(os.path.join(path,fname),'r', encoding='utf-8') as f:
#         train_texts.append(f.read())
#   random.seed(seed)
#   random.shuffle(train_texts)
#   return train_texts
# train_texts = load_data(path,seed)

def load_data(path,seed):
  train_texts = []
  with open('./Articles/ARMY_SPO.20210317.clean.filtered','r', encoding='utf-8') as f:
      data = f.readlines()
      for d in data:
          train_texts.append(d.strip().split('\t')[0].replace('_', ' '))
          train_texts.append(d.strip().split('\t')[1].replace('_', ' '))
  random.seed(seed)
  random.shuffle(train_texts)
  return train_texts
train_texts = load_data(path,seed)


"""### Tokenizing the document and filtering the tokens"""

def tokenize(train_texts):
  filtered_tokens = []
  tokens = [word for sent in train_texts for word in sent.split(' ')]
  for token in tokens:
      filtered_tokens.append(token)
  return filtered_tokens


"""### Tokenizing and stemming using Snowball stemmer"""

# def tokenize_stem(train_texts):
#   tokens = tokenize(train_texts)
#   stemmer = SnowballStemmer('english')
#   stemmed_tokens = [stemmer.stem(token) for token in tokens]
#   return stemmed_tokens



"""### Generating the vocab for problem statement"""

# def generate_vocab(train_texts):
#   vocab_tokenized = []
#   vocab_stemmed = []
#   total_words = []
#   for text in train_texts:
#     allwords_tokenized = tokenize(text)
#     total_words.append(allwords_tokenized)
#     vocab_tokenized.extend(allwords_tokenized)
#     allwords_stemmed = tokenize_stem(text)
#     vocab_stemmed.extend(allwords_stemmed)
#   return vocab_tokenized,vocab_stemmed,total_words
# vocab_tokenized,vocab_stemmed,total_words = generate_vocab(train_texts)


"""### Calculating Tf-idf matrix"""

'''
Attributes in TfidVectorizer are data dependent.
Use 'stop_words = customized_stopwords' if you want to use your own set of stopwords else leave it as it is.
Functions available for tokenizer -> 1)tokenize  2) tokenize_stem  3) Remove the attribute to use default function
'''
print(len(train_texts))
def tfid_vector(train_texts):
  tfidf_vectorizer = TfidfVectorizer(max_df = 0.85, min_df = 0.1, sublinear_tf = True, use_idf = True, tokenizer = tokenize, ngram_range = (1,10))
  tfidf_matrix = tfidf_vectorizer.fit_transform(train_texts)
  return tfidf_matrix
tfidf_matrix = tfid_vector(train_texts)


"""### Clustering Using K - Means"""

#Code For Elbow Method
nc = range(1,5)
kmeans = [KMeans(n_clusters = i, n_init = 100, max_iter = 500, precompute_distances = 'auto' ) for i in nc]
score = [kmeans[i].fit(tfidf_matrix).score(tfidf_matrix) for i in range(len(kmeans))]
plt.plot(nc,score)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.savefig("elbow_curve.png")


#Uncomment the below code after getting appropriate k value from the graph

# K_value = int(input("Enter Optimum K Value = "))      #Write the optimum K-value after seeing the Elbow Graph
# km = KMeans(n_clusters = K_value, n_init = 2000, max_iter = 6000, precompute_distances = 'auto' )
# clusters = km.fit_predict(tfidf_matrix)
# clusters = list(clusters)
# print(clusters)
#
# if 'Results' not in os.listdir(os.getcwd()):
#     os.mkdir('Results')
#
#
# cluster_dict = {}
# for c,t in zip(clusters, train_texts):
#     if c in cluster_dict:
#         if t not in cluster_dict[c]:
#             cluster_dict[c].append(t)
#     else:
#         cluster_dict[c] = [t]
#
#
# for key in cluster_dict:
#     with open('./Results/cluster_{}.txt'.format(str(key)), 'w', encoding='utf-8') as file:
#         for data in cluster_dict[key]:
#             file.write(data.replace('_', '')+'\n')

