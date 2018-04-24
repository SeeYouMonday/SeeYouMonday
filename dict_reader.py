import csv
from pprint import pprint
from itertools import groupby
from operator import itemgetter

def csv_to_dictList(file):
    reader = csv.DictReader(open(file, 'r'))
    dictList = [line for line in reader]
    # pprint(dictList)
    # print(dictList[0]["Url"])
    # print(len(dictList))
    return dictList

# l = csv_to_dictList("crawl/monster-software engineer-boston-ma-job-results.csv")
#
# # urls = itemgetter("Url")
# # print(urls)
#
# result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in l)]
# print(len(result))