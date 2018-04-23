from lxml import html
import requests
import re
import os
import sys
import unicodecsv as csv
import argparse
import json


def indeed_crawl(keyword, city, state):
    print("Fetching {} at {},{}".format(keyword, city, state))

    # convert place id
    place_id = "{}%2C+{}".format(city, state)

    # Form GET request like this one
    # https://www.monster.com/jobs/search/?q=software-engineer&where=Boston__2C-MA&page=1
    job_litsting_url = 'https://www.indeed.com/jobs'
    params = {
        'q': keyword,
        'l': place_id
    }
    response = requests.get(job_litsting_url, params=params)

    # Extract data
    parser = html.fromstring(response.text)

    # Making absolute url
    base_url = "https://www.monster.com/"
    parser.make_links_absolute(base_url)

    XPATH_ALL_JOB = '//div[@class="summary"]'
    XPATH_NAME = './/a/text()'
    XPATH_JOB_URL = './/a/@href'
    XPATH_LOC = './/div[@class="location"]/span/text()'
    XPATH_COMPANY = './/div[@class="company"]/span/text()'

    # Loop to get each job posting
    job_listings = []
    listings = parser.xpath(XPATH_ALL_JOB)
    for job in listings:
        raw_job_name = job.xpath(XPATH_NAME)
        raw_job_url = job.xpath(XPATH_JOB_URL)
        raw_lob_loc = job.xpath(XPATH_LOC)
        raw_company = job.xpath(XPATH_COMPANY)

        # Clean name
        job_name = ''.join(raw_job_name).replace('*', '').strip() if raw_job_name else None

        # Clean location
        job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
        raw_state = re.findall(",\s?(.*)\s?", job_location)
        state = ''.join(raw_state).strip()
        raw_city = job_location.replace(state, '')
        city = raw_city.replace(',', '').strip()

        # Clean company name
        company = ''.join(raw_company).replace('–', '')

        # Clean job url
        job_url = raw_job_url[0] if raw_job_url else None

        jobs = {
            "Name": job_name,
            "Company": company,
            "City": city,
            "State": state,
            "Url": job_url
        }
        job_listings.append(jobs)

    return job_listings



if __name__ == "__main__":

    ''' eg-:python whatever.py "Android developer" "new york" "NY" '''

    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword', help='job name', type=str)
    argparser.add_argument('city', help='job location', type=str)
    argparser.add_argument('state', help='state location', type=str)
    args = argparser.parse_args()
    keyword = args.keyword
    city = args.city
    state = args.state
    # keyword = "software-engineer"
    # city = "Boston"
    # state = "MA"
    scraped_data = indeed_crawl(keyword, city, state)
    # print(scraped_data)

    print("Writing data to output file")
    with open('monster-{}-{}-{}-job-results.csv'.format(keyword, city, state), 'wb')as csvfile:
        fieldnames = ['Name', 'Company', 'City', 'State', 'Url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        if scraped_data:
            for data in scraped_data:
                writer.writerow(data)
        else:
            print("Your search for {}, in {},{} does not match any jobs".format(keyword, city, state))
