import re
import json 
import PorterStemmer

with open('keywords.json', 'r') as f: 
  dictionary = json.load(f)
  f.close()

def tokenize(text):
  clean_string = re.sub('[^a-z0-9- ]', ' ', text.lower())
  tokens = clean_string.split()
  return tokens

def stemming(self, tokens):
  stemmed_tokens = []
  # PUT YOUR CODE HERE
  stemmer = PorterStemmer.PorterStemmer()
  stemmed_tokens = [stemmer.stem(t, 0, len(t) - 1) for t in tokens]
  return stemmed_tokens

def index(tokens):
  mp = {}
  for t in tokens:
    for k,v in dictionary.items():
      if t in v:
        mp[k] = mp.get(k, 0) + 1 
  return mp

def normalize(d):
  sum_vals = sum(d.values())
  for k, v in d.items():
    d[k] = v * 1.0 / sum_vals
  return d 


def return_index(file_path='parse/outputtext.txt'):
  with open(file_path, 'r') as f:
    text = f.read()
    f.close()
  
  tokenized = tokenize(text)
  indexed = index(tokenized)
  normalized = normalize(indexed)
  return normalized

if __name__ == "__main__":
  file_path = 'parse/outputtext.txt'
  return_index(file_path)