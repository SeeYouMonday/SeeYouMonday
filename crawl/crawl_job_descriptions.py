import re
import parse_pdf.PorterStemmer as PorterStemmer
import urllib.request
import numpy as np
from urllib.parse import urlparse
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup, SoupStrainer

def tokenize(text):
  clean_string = re.sub('[^a-z0-9- ]', ' ', text.lower())
  tokens = clean_string.split()
  return tokens


def stemming(tokens):
  stemmed_tokens = []
  # PUT YOUR CODE HERE
  stemmer = PorterStemmer.PorterStemmer()
  stemmed_tokens = [stemmer.stem(t, 0, len(t) - 1) for t in tokens]
  return stemmed_tokens

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def crawl_text(url):
    #try:
    url = urllib.parse.quote(':')
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(page, "html.parser")

    # prepare doc text
    # text = soup.find(id="JobDescription").get_text()
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts) 

    doc_stemmed_tokens = set(stemming(tokenize(visible_texts)))
    print(doc_stemmed_tokens)



def get_urls(filename):
    d = Documents()

    with open(filename, 'r') as f:
        list = [line.split(',') for line in f]        # create a list of lists
        list = list[1:]
        for i,x in enumerate(list):              #print the list items 
            job = Job(x)
            if 'glassdoor' in filename:
                job.url = x[5]
            d.jobs.append(job)

    for j in d.jobs:
        print(j.title)
        print(j.company)
        print(j.state)
        print(j.city)
        print(j.url)
        description = crawl_text(j.url)
        print(description)
        break


class Job():
    def __init__(self, list):
        self.title = list[0] 
        self.company = list[1]
        self.state = list[2]
        self.city = list[3]
        self.url = list[4]


class Documents():
    def __init__(self):
        self.jobs = [] # list of jobs 
        self.documents = [] # list of Jobs 


if __name__ == "__main__":
    glassdoor_file = 'crawl/glassdoor-software-engineer-worcester-job-results.csv'
    monster_file = 'crawl/monster-software-engineer-boston-ma-job-results.csv'
    get_urls(monster_file)