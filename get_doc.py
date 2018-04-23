from crawl.monster_crawl import monster_crawl
from crawl.glassdoor_crawl import glassdoor_crawl
import itertools

positions = ["software-engineer", "data-scientist"]
cities = ["San-Francisco", "Boston"]
states = ["CA", "MA"]

job_list = []

# get the job listings
for position in positions:
    for city_idx in range(len(cities)):
        job_list.append(monster_crawl(position, cities[city_idx], states[city_idx]))

# flatten the job list
flatten_job_list = list(itertools.chain.from_iterable(job_list))

# for job in flatten_job_list:
    