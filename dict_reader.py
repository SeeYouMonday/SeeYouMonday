import csv
from pprint import pprint

def csv_to_dictList(file):
    reader = csv.DictReader(open(file, 'r'))
    dictList = [line for line in reader]
    # pprint(dictList)
    # print(dictList[0]["Url"])
    return dictList

