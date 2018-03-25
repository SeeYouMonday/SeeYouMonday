# import bs4 as BeautifulSoup  # you will want this for parsing html documents
import re
import urllib.request
import numpy as np
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer


# our index class definition will hold all logic necessary to create and search
# an index created from a web directory
#
# NOTE - if you would like to subclass your original Index class from homework
# 1 or 2, feel free, but it's not required.  The grading criteria will be to
# call the index_url(...) and ranked_search(...) functions and to examine their
# output.  The index_url(...) function will also be examined to ensure you are
# building the index sanely.

# helper to parse the url 
def parse_url(url):
    # parse out the page name and base_url
    last_slash_idx = url.rfind('/')
    doc_name = url[last_slash_idx + 1:]
    base_url = url[:last_slash_idx + 1]
    return base_url, doc_name 

# helper function to normalize the matrix
def normalize_matrix(matrix):
    row_sums = matrix.sum(axis=1)
    normalized_matrix = matrix / row_sums[:, np.newaxis]
    return normalized_matrix

class PageRankIndex(object):
    def __init__(self):
        # you'll want to create something here to hold your index, and other
        # necessary data members
        self.doc_urls = [] # list to hold doc urls (enable getting indices of the docs)  
        self.documents = {} # map to hold doc id and html page 
        self.doc_graph = {} # map to hold doc url and the other links inside the doc
        self.inverted_index = {} # map for inverted index: term - posting lists 

        self.alpha = 0.1
        self.transition_matrix = None

        self.rank_scores = None # list to hold page rank scores
        

    # index_url( url )
    # purpose: crawl through a web directory of html files and generate an
    #   index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: use BeautifulSoup and urllib
    # parameters:
    #   url - a string containing a url to begin indexing at
    def index_url(self, url):
        # if have seen this page, skip 
        if url in self.doc_urls:
            return len(self.doc_urls)

        self.doc_urls.append(url)
        base_url, doc_name = parse_url(url)
        
        # read the web page
        with urllib.request.urlopen(url) as read_url:
            html_page = read_url.read()
        
        soup = BeautifulSoup(html_page, "html.parser")
        # index the web page content
        # self.doc_urls.append(url)
        doc_idx = self.doc_urls.index(url)
        self.build_inverted_index(doc_idx, soup.get_text())

        # initialize current graph node
        # the graph holds the url instead of index because we won't know the indices until we finish
        self.doc_graph[url] = []

        # call index_url for the anchor texts in the current page
        for link in BeautifulSoup(html_page, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'): 
                l = link.get('href')
                # check if it is a relative url
                if l[:4] != 'http':
                    l = base_url + l 

                # add neighbors to the node in the graph 
                self.doc_graph[url].append(l)
                

        return len(self.doc_urls)

    # build inverted index
    def build_inverted_index(self, doc_id, doc_text):
        tokens = self.tokenize(doc_text)
        for t in tokens:
            if t not in self.inverted_index:
                self.inverted_index[t] = set()
            self.inverted_index[t].add(doc_id)
        
    # tokenize( text )
    # purpose: convert a string of terms into a list of terms 
    # preconditions: none
    # returns: list of terms contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        # ADD CODE HERE
        clean_string = re.sub('[^a-z0-9 ]', ' ', text.lower())
        tokens = clean_string.split()
        return tokens

    # calculate_transition_matrix()
    # defined by Anqi Lu
    # purpose: calculate the transition matrix with teleporting
    def calculate_transition_matrix(self):
        l = len(self.doc_urls)
        teleport_matrix = np.ones((l, l))
        link_matrix = np.zeros((l, l))

        # corresponding link matrix
        for node, neighbors in self.doc_graph.items():
            node_idx = self.doc_urls.index(node)
            for n in neighbors:
                neighbor_idx = self.doc_urls.index(n)
                link_matrix[node_idx][neighbor_idx] += 1

        # normalize both matrices
        teleport_matrix = normalize_matrix(teleport_matrix)
        transition_matrix = normalize_matrix(link_matrix)

        # add teleporting 
        self.transition_matrix = transition_matrix * (1.0-self.alpha) + teleport_matrix * self.alpha
        
        return 

    def matrix_converge(self):
        threshold = 1e-3
        max_iter = 1000
        x = np.ones((len(self.doc_urls))) /  len(self.doc_urls)

        next_x = x.dot(self.transition_matrix)

        for i in range(max_iter):
            diff = np.sum(np.abs(next_x - x))
            if diff < threshold:
                self.rank_scores = next_x
                return 
            x, next_x = next_x, next_x.dot(self.transition_matrix)
        
        self.rank_scores = next_x
        return 

    # ranked_search( text )
    # purpose: searches for the terms in "text" in our index and returns
    #   AND results for highest 10 ranked results
    # preconditions: .index_url(...) has been called on our corpus
    # returns: list of tuples of (url,PageRank) containing relevant
    #   search results
    # parameters:
    #   text - a string of query terms
    def ranked_search(self, text):
        results_set = set(range(0, len(self.doc_urls)))
        search_terms = self.tokenize(text)

        for term in search_terms: 
            # if one of the terms not in the doc - no result
            if term not in self.inverted_index:
                results_set = set()
            else:
                results_set = results_set.intersection(set(self.inverted_index.get(term)))
        
        return results_set 
        """
        results = []
        
        
        for r in results_set:
            score = np.round(self.rank_scores[r], 4)
            # add the name of the webpage and score
            base_url, name = parse_url(self.doc_urls[r]) 
            results.append((name, score))

        sorted_results = sorted(results, key=lambda tup: tup[1], reverse=True)
        return sorted_results
        """


# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    index = PageRankIndex()
    url = 'https://www.indeed.com/jobs?q=software+engineer&l='

    num_files = index.index_url(url)

    ### added code  
    # index.calculate_transition_matrix()
    # index.matrix_converge()
    ### End of my added code 
    print(index.doc_urls)
    # print(index.inverted_index)
    search_queries = (
       'java', 'python ', 'software development', 'big data', 'machine learning'
        )
    for q in search_queries:
        results = index.ranked_search(q)
        print("searching: %s -- results: %s" % (q, results))


# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

