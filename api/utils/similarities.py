import torch
from math import sqrt, pow, exp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
#from api.utils.models import model, tokenizer


"""Here are the similarity metrics"""

#Lexical Similarity - keywords matter in CVs or job descriptions
#1. Jaccard similarity : How much unique words are shared? (frequency doesn't matter)
def jaccard_similarity(x, y):
  """ returns the jaccard similarity between two texts """
  sentences = x, y
  x, y = [sent.lower().split(" ") for sent in sentences]
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)

#2. TF-IDF & Cosine similarity : How much important terms and focuses do they share? 
def tfidf_similarity(x, y):
  """ returns the cosine similarity between TF-IDF of two texts """
  vectorizer = TfidfVectorizer()
  tfidf_matrix = vectorizer.fit_transform([x, y])
  document_vectors = tfidf_matrix.toarray()       #scarce vector
  return cosine_similarity(document_vectors)[0][1]



#Semantic Similarity - what points are the documents making
#3. Embedding & Cosine similarity: How are they semantically similar?
@torch.no_grad()    # Decorator to disable gradient calculations
def get_embeddings(docs: List[str], model, tokenizer, input_type:str='document') -> List[List[float]]:
    # Prepend retrieval instruction to queries
    # if input_type == "query":
    #     docs = ["{}{}".format(RETRIEVAL_INSTRUCT, q) for q in docs]
    # Tokenize input texts
    inputs = tokenizer(docs, padding=True, truncation=True, return_tensors='pt', max_length=512)#.to(device)
    # Pass tokenized inputs to the model, and obtain the last hidden state
    last_hidden_state = model(**inputs, return_dict=True).last_hidden_state
    # Extract embeddings from the last hidden state
    embeddings = last_hidden_state[:, 0]
    return embeddings.cpu().numpy()

def embeddings_similarity(x, y, model, tokenizer):
   embeddings1 = get_embeddings([x], model, tokenizer)
   embeddings2 = get_embeddings([y], model, tokenizer)
   return cosine_similarity(embeddings1, embeddings2)[0][0]


















# def euclidean_distance(x, y):
#   """ returns the euclidean distance between two texts """
#   a = len(x)
#   b = len(y)
#   dist = numpy.linalg.norm(a-b)
#   return dist

# def distance_to_similarity(distance):
#   """converts distnace into similarity"""
#   return 1/exp(distance)

# def euclidean_distance_similarity(x, y):
#   """converts euclidean distance into similarity score"""
#   return distance_to_similarity(euclidean_distance(x, y))









