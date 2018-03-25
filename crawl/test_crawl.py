import re
import urllib.request
import numpy as np
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer

url = "https://www.indeed.com/q-software-engineer-jobs.html" 

base_url = "https://www.indeed.com"
with urllib.request.urlopen(url) as read_url:
    html_page = read_url.read()
    
soup = BeautifulSoup(html_page, "html.parser")
divTag = soup.find_all("div", {"class": "row result"})

#print(divTag)

for tag in divTag:
    tdTags = tag.find_all("a", {"class": "jobtitle"})

    for tag in tdTags:
        print(tag.text)
        l = tag.get("href")
        if l[:4] != 'http':
             l = base_url + l 

# call index_url for the anchor texts in the current page
# for link in BeautifulSoup(html_page, "html.parser", parse_only=SoupStrainer('a')):
#     if link.has_attr('href'): 
#         l = link.get('href')

#         # check if it is a relative url
#         if l[:4] != 'http':
#             l = base_url + l 