import csv
import pandas as pd

# with open('data/computer-systems.csv', 'r') as csvfile:

def parse_terms(s):
    s = s[s.find("{")+1:s.find("}")]
    strlist = s.split(', ')
    strlist = [str[1:-1] for str in strlist]
    return strlist

def new_dataframe():
    df = pd.read_csv('data/computer-systems.csv')

    print(df['Terms'][:3])

    for i, x in enumerate(df['Terms']):
        df['Terms'][i] = parse_terms(x)
    return df

if __name__ == "__main__":
    new_df = new_dataframe()