import csv
import json
import pandas as pd
import numpy as np

K_TOP_RESULTS = 20


def parse_terms(s):
    s = s[s.find("{")+1:s.find("}")]
    strlist = s.split(', ')
    strlist = [str[1:-1] for str in strlist]
    return strlist


def new_dataframe(df):
    for i, x in enumerate(df['Terms']):
        df['Terms'][i] = parse_terms(x)
    return df


def match(user_tokens, df):

    job_list = new_dataframe(df)
    # get keywords
    with open('keywords.json', 'r') as f:
        keywords = set(json.load(f))
        f.close()

    resume_tokens_set = set(user_tokens)
    resume_terms = keywords & resume_tokens_set

    # calculate similarity scores
    print("Calculating similarities")
    scores = []

    for index, job in job_list.iterrows(): 
        doc_terms = set(job['Terms'])
        # calculate Jaccard
        intersect_score = float(len(doc_terms & resume_terms))
        union_score = float(len(doc_terms | resume_terms))
        jaccard_score = intersect_score / union_score

        # save the score
        job["Score"] = jaccard_score
        scores.append(jaccard_score)

    # rank by similarity scores
    sorted_args = np.argsort(scores)[::-1]

    results = job_list.loc[sorted_args[:K_TOP_RESULTS]] 
    return results

if __name__ == "__main__":
    df = pd.read_csv('data/computer-systems.csv')
    user_tokens = ['experience', 'daniel', 'song', '112', 'willow', 'st', 'acton', 'ma', '978-319-1368', \
     'dansong01', 'gmail', 'com', 'http', 'users', 'wpi', 'edu', 'dlsong', 'https', 'github', 'com', \
     '1nkling', 'august', '2017', 'present', 'software', 'engineer', 'mit', 'lincoln', 'laboratories',\
      'implemented', 'optimized', 'image', 'processing', 'algorithms', 'nuc', 'cfar', 'on', 'jetson',\
       'tx1', 'tx2', 'boards', 'in', 'cuda', 'c++', 'for', 'an', 'autonomous', 'closed-loop', 'cubesat', \
       'optical', 'sensor', 'system', 'june', '2017', 'august', '2017', 'applications', 'engineering',\
        'intern', 'silicon', 'labs', 'created', 'sample', 'applications', 'in', 'c', 'to', 'demonstrate', \
        'the', 'functionality', 'of', 'proprietary', 'radio', 'boards', 'using', 'zigbee', 'thread', 'protocols', \
        'to', 'potential', 'customers', 'currently', 'in', 'use', 'by', 'ring', 'lutron', 'and', 'more', \
        'education', 'august', '2014', '-', 'present', 'b', 's', 'electrical', 'and', 'computer', 'engineering', \
        'ece', 'minor', 'in', 'computer', 'science', 'cs', 'worcester', 'polytechnic', 'institute', 'wpi', 'worcester', \
        'ma', 'gpa', '3', '77', 'graduating', 'on', 'may', '2018', 'cs', 'coursework', 'introduction', 'to', \
        'program', 'design', 'object-oriented', 'design', 'concepts', 'systems', 'programming', 'concepts', 'machine', \
        'org', 'assembly', 'algorithms', 'tbc', 'spring', '2018', 'database', 'systems', 'i', 'ii', 'artificial', \
        'intelligence', 'computer', 'networks', 'ece', 'coursework', 'digital', 'circuit', 'design', 'digital', 'system', \
        'design', 'with', 'fpgas', 'embedded', 'computing', 'in', 'engineering', 'design', 'real', 'time', 'embedded', 'systems', 'continuous', 'discrete', 'time', 'analysis', 'skills', 'programming', 'languages', 'racket', 'java', 'c', 'c++', 'computer', 'skills', 'android', 'studios', 'eclipse', 'cuda', 'css', 'html', 'xml', 'communication', 'protocols', 'zigbee', 'thread', 'github', 'git', 'bash', 'cmd', 'terminal', 'putty', 'sublime', 'text', 'emacs', 'multisim', 'matlab', 'verilog', 'projects', 'jane', 'hack', 'wpi', 'january', '2017', 'created', 'an', 'interactive', 'facebook', 'bot', 'using', 'python', 'that', 'could', 'get', 'weather', 'info', 'provide', 'images', 'of', 'specific', 'objects', 'translate', 'between', 'several', 'languages', 'and', 'much', 'more', 'sustain', 'wpi', 'iq', 'project', 'fall', '2016', 'created', 'an', 'android', 'application', 'that', 'uses', 'responses', 'to', 'dynamically', 'generated', 'questions', 'to', 'determine', 'an', 'individual', 's', 'level', 'of', 'environmental', 'sustainability', 'and', 'recommend', 'improvements']
    match(user_tokens, df)