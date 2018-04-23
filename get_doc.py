from crawl.monster_crawl import monster_crawl
from crawl.glassdoor_crawl import glassdoor_crawl
import parse_pdf.PorterStemmer as PorterStemmer
import itertools
import bs4 as BeautifulSoup
import urllib.request
import urllib.parse
import numpy as np
import json
import re
from tqdm import tqdm
import time


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


def get_doc():
    # positions = ["software-engineer", "data-scientist"]
    # cities = ["San-Francisco", "Boston"]
    # states = ["CA", "MA"]

    positions = ["software-engineer"]
    cities = ["San-Francisco"]
    states = ["CA"]

    job_list = []

    # get the job listings
    for position in positions:
        for city_idx in range(len(cities)):
            job_list.append(monster_crawl(position, cities[city_idx], states[city_idx]))

    # flatten the job list
    flatten_job_list = list(itertools.chain.from_iterable(job_list))

    # get keywords
    with open('keywords.json', 'r') as f:
      keywords = set(stemming(json.load(f)))
      f.close()

    # prepare sample resume
    sample_resume = [
        "java", "javascript", "js", "sql",
        "html", "css", "bootstrap", "react", "ajax", "json", "d3", "node", "api", "website", "ui",
        "object", "oriented", "agile", "git", "algorithms", "design", "software",
        "bachelor"]
    resume_stemmed_tokens = set(stemming(sample_resume))
    resume_terms = keywords & resume_stemmed_tokens

    # calculate similarity scores
    print("Calculating similarities")
    scores = []
    for job in tqdm(range(len(flatten_job_list))):
        time.sleep(15) # per robot.txt request
        try:
            # parse
            page = urllib.request.urlopen(flatten_job_list[job]["Url"])
            soup = BeautifulSoup.BeautifulSoup(page, "html5lib")

            # prepare doc text
            text = soup.find(id="JobDescription").get_text()
            doc_stemmed_tokens = set(stemming(tokenize(text)))
            doc_terms = keywords & doc_stemmed_tokens

            # calculate Jaccard
            intersect_score = float(len(doc_terms & resume_terms))
            union_score = float(len(doc_terms | resume_terms))
            jaccard_score = intersect_score / union_score

            # save the score
            flatten_job_list[job]["Score"] = jaccard_score
            scores.append(jaccard_score)
        except:
            # print("Something went wrong, make score = -1 and skip this url")
            flatten_job_list[job]["Score"] = -1
            scores.append(-1)

    # rank by similarity scores
    argsort = np.argsort(scores)[::-1]

    # display
    print("Results")
    for i in argsort:
        print(flatten_job_list[i])


if __name__ == "__main__":
  get_doc()