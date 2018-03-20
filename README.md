# See You Monday

CS525 Informational Retrieval & Social Web Project 

Professor [Kyumin Lee](http://web.cs.wpi.edu/~kmlee/)

Spring 2018

Worcester Polytechnic Institute


## Authors 

- Khuyen Cao
- Quyen Hoang
- [Anqi Lu](https://github.com/anqi-lu)

## Introduction & Motivation

Every year, many people have the need to look for internships or part-time/full-time jobs at companies. We all have experienced the long and stressful process of searching for positions to apply to on the internet. Existing job posting search engines like Glassdoor and Indeed crawls a great volume of job postings from all over the web. Job seekers could define parameters such as position type and location to narrow the search. However, the users of these tools still have to click into every result and read through the descriptions to determine whether the posting is fit for them, which is a tiring and time-consuming process. We would like to propose a personalized job searching tool called See You Monday (SUM) where the results are tailored to individual users based on their resume. Using SUM, the user can upload a resume in pdf format. The data available from that input resume will be parsed through the text to identify user’s skill set, and match the skill set with our documents that we have already built by crawling current top job searching tools such as Glassdoor and Indeed. The return results will be kept at a small k number (10-20) for easier navigation, ranked from most to least relevant to the input resume. For this project, we limit the search parameters for only Computer Science related jobs due to the restricted time and resources. This can benefit all people in tech field who want to find a job match by saving their time and energy. In future work, we can expand this tools to match different careers and can furthermore benefit a larger range of users.

## Methodology 

### Data Acquisition

Scope: We limit the job field to Computer Science only, and will support both internship and full-time job search. We will crawl the top 3 job sites: Indeed, Monster and Glassdoor. We will create a list of potential job titles and iterative through the list by changing query parameters on the urls to crawl. (For example: https://www.monster.com/jobs/search?q=software-engineer) Each job posting would be a document and we will store the job title, company name, location, and job description. We will crawl around 500 job postings from each website. This number may vary depending on the websites’ crawling policy.

### Tools and methods

* Website building and hosting service: we plan to host our web application on Github Pages in consistent with having all our codes available there. The web front-end uses conventional HTML and CSS with Bootstrap. The backend uses python web server pipelining.

* Programming language: Python 3.6

* Parsing pdf input: we plan to use an existing pdf parsing tools called [PDFMiner](https://github.com/pdfminer/pdfminer.six) . PDFMiner is free, open source and available on Github. It is compatible with both Python 2 and 3, with a focus on parsing and analyzing text data, which is suitable for the goal of our project. Additionally, PDFMiner supports multiple font types and allow us to convert the PDF input files into plain text format.

* Ranking: tf-idf and cosine similarity. We will index the documents as we have done for the homeworks. But instead of using the full vocabulary, we will create a much smaller dictionary containing only tech related keywords that appear often on resumes and company websites, as technical skills are what companies are mostly looking for. We will also manually create equivalent term dictionary for technical terms that have multiple variations. For example, “NLP” and “natural language processing” would be considered the same term. 

## Results and evaluation

We plan to finish building the web-app at least 1-2 weeks before the due date for the final project and use our own resume for first step evaluation. We will select one of our resumes and randomly select 20 documents. Since most of the documents will potentially be relevant based on our scope, we will not calculate precision and recall. We will  rank the documents on scale of 0-3 manually, so we will have a best order of documents and a ground truth Discounted Cumulative Gain(DCG) value. From there we can calculate the Normalized DCG of our system. 
  
We will also pass out the link to SUM for friends and fellow students at WPI for evaluation. There can be a quick survey at the end of the website for users to give us feedbacks. The accuracy of the results can be based on the precision score of users' feedbacks on how many jobs, out of the total return results, that the users really want to apply. We expect to have around 20+ feedbacks to have an estimates of how well the tools that we built performed from a user perspective. Additional adjustment will be made if the results is not desirable.

## Limitations and future scopes

Our tool however, will be very preliminary for its use. It has the following limitations (also the challenges of building such system): 
* (a) We are only taking technical terms in the assumption that companies only care about the technology, but it’s not always the case. 

* (b) Big websites Glassdoor and Indeed are already very powerful in crawling company websites at a certain rate (at least once a day). We don’t have the computing power and storage, so our project will only have a small subset of the documents that are not updated frequently. 

In the future, we could explore abstracting one person’s experience and skill sets and match with the company and postings in a natural language processing way. This will not only help SUM give a more accurate match but also largely widen the range of our target users. 




