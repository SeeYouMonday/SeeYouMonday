# See You Monday

CS525 Informational Retrieval & Social Web Project 
Professor [Kyumin Lee](http://web.cs.wpi.edu/~kmlee/)
Spring 2018
Worcester Polytechnic Institute

Link to See You Monday(SUM): [https://see-you-monday.herokuapp.com/](https://see-you-monday.herokuapp.com/)

## Authors 

- [Khuyen Cao](https://github.com/hakhuyen1997)
- [Quyen Hoang](https://github.com/quyendinhthuchoang)
- [Anqi Lu](https://github.com/anqi-lu)

## Introduction & Motivation

Every year, many people have the need to look for internships or part-time/full-time jobs at companies. We all have experienced the long and stressful process of searching for positions to apply to on the internet. Existing job posting search engines like Glassdoor and Indeed crawls a great volume of job postings from all over the web. Job seekers could define parameters such as position type and location to narrow the search. However, the users of these tools still have to click into every result and read through the descriptions to determine whether the posting is fit for them, which is a tiring and time-consuming process. We would like to propose a personalized job searching tool called See You Monday (SUM) where the results are tailored to individual users based on their resume. Using SUM, the user can upload a resume in pdf format. The data available from that input resume will be parsed through the text to identify user’s skill set, and match the skill set with our documents that we have already built by crawling current top job searching tools such as Glassdoor and Indeed. The return results will be kept at a small k number (20) for easier navigation, ranked from most to least relevant to the input resume. For this project, we limit the search parameters for only Computer Science related jobs due to the restricted time and resources. This can benefit all people in tech field who want to find a job match by saving their time and energy. In future work, we can expand this tools to match different careers and can furthermore benefit a larger range of users.

## Methodology 

### Data Acquisition

We limit the job field to Computer Science only. We attempted to crawl from 3 top job sites: Indeed, Monster and Glassdoor. With Monster, we were able to get 250 results from one go; with Glassdoor, we only get 25 results at a time; with Indeed, we only got 10 results. 

We created a list of potential job titles and iterative through the list by changing query parameters on the urls to crawl. 
Even though we limited the scope to Computer Science related, there are still sub-fields of job positions. We used
"Software Engineer", "Data Scientist", and "Computer Systems" as three keywords we used to crawl since these three fields
seem to capture a lot of Computer Science job positions and also have little overlap. 

 Each job posting contains job title, company name, location, url, and job description terms. In total, crawled around 600 job postings. It is stored in "out.csv" in "data" folder. 

### Tools and methods

* Website building and hosting service: we plan to host our web application on Github Pages in consistent with having all our codes available there. The web front-end uses conventional HTML and CSS with Bootstrap. The backend uses python web server pipelining.

* Programming language: Python 3.6

* Parsing pdf input: we plan to use an existing pdf parsing tools called [PDFMiner](https://github.com/pdfminer/pdfminer.six) . PDFMiner is free, open source and available on Github. It is compatible with both Python 2 and 3, with a focus on parsing and analyzing text data, which is suitable for the goal of our project. Additionally, PDFMiner supports multiple font types and allow us to convert the PDF input files into plain text format.

* Ranking: [Jaccard similarity](https://en.wikipedia.org/wiki/Jaccard_index). We indexed the documents as we have done for the homeworks. But instead of using the full vocabulary, we created a much smaller dictionary containing only tech related keywords that appear often on resumes and company websites, as technical skills are what companies are mostly looking for. We also included technical terms that have multiple variations. For example, “NLP” and “natural language processing” are both in our dictionary. The Jaccard similarity measures the overlap unique technical terms between the resume and the job positing. The resulting job postings were ranked in descending order. 

## Results and evaluation

 We randomly select 12 documents from our data file as a test document collection. Since most of the documents will potentially be relevant based on our scope, we do not calculate precision and recall. We ranked the documents on scale of 0-3 manually, so we had a best order of documents and a ground truth Discounted Cumulative Gain(DCG) value. From there we can calculate the Normalized DCG of our system. The score from NDCG seems promising. 
  
> SUM Ranking:
3 1 3 1 1 3 0 2 1 0 0 0

> Ground Truth Ranking: 
3 3 3 2 1 1 1 1 0 0 0 0 

> NDCG@5: 0.82 

> NDCG@12: 0.95

We also advocated link to SUM for friends and fellow students at WPI for evaluation. There is a quick survey at the end of the website for users to give us feedbacks. In the survey we asked the following questions:
* Your overall satisfaction of this page? (Rate 1 - 5)
* How helpful do you think it was for finding your job? (Rate 1 - 5)
* Was the website easy for you to navigate? (Rate 1 - 5)
* The percentage of the results in which you find closely match your need? (<25%, 25-50%, 50-75%, >75%)
* How many links in the results that you clicked? 
* Will you use "See U Monday" as a job searching tool next time? (Yes, No, Maybe)
* Will you recommend "See U Monday" to a friend? (Yes, No, Maybe)
* Additional feedback (Optional)

We collected around 20 feedbacks to have an estimates of how well the tools that we built performed from a user perspective.
Findings from the user study survey:
* 67% participants are satisfied with our website.
* 58% participants think SUM is helpful in job searching.
* 81% participants think SUM is easy to navigate.
* 47.6% participants will recommend SUM to friends, and 47.6% chose "maybe". 



## Discussion

* It is difficult to crawl websites. Most famous websites have mechanism to prevent people from crawling a lot of results from their websites too frequently. Once we crawled job postins on Monster without sleeping, our IPs were blocked by Monster. So we used VPN and add 15 seconds of sleeping to crawl between job postings. One take-away is that we should respect and follow the crawling guideline set by other websites. 

* We had a discussion about what measures we should use to calculate the similalrity between job postings and resumes. The potential options were: cosine similarity, tf-idf, Jaccard similarity, and Pearson similarity. We decided that term frequency didn't matter that much for resumes and job postings so we decided not to use tf-idf. We wanted a measure that captures how well one's technical skills fit with job's technical requirements. Jaccard similarity seems to be the way to go as it captures the overlap between two sets divided by the union of the two sets.

## Limitations and future scopes

Our tool however, will be very preliminary for its use. It has the following limitations (also the challenges of building such system): 
* (a) We are only taking technical terms in the assumption that companies only care about the technology, but it’s not always the case. 

* (b) Big websites Glassdoor and Indeed are already very powerful in crawling company websites at a certain rate (at least once a day). We don’t have the computing power and storage, so our project will only have a small subset of the documents that are not updated frequently. 

In the future, we could explore abstracting one person’s experience and skill sets and match with the company and postings in a natural language processing way. This will not only help SUM give a more accurate match but also largely widen the range of our target users. 


## Instruction to run it
* install pipenv to create virtual environment 
> `pip install pipenv`
* install packages in pipfile
> `pipenv install`
* activate virtual environment
> `pipenv shell`

* To serve the web locally
> `python app.py`

Again, website is also hosted on heroku at [https://see-you-monday.herokuapp.com/](https://see-you-monday.herokuapp.com/)
