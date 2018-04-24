import matplotlib as plt
import csv
import pandas as pd
import itertools


df = pd.read_csv('data-scientist.csv', encoding='utf-8')
terms_column = df['Terms'] 
terms_list = [terms for terms in terms_column]

print(terms_list)