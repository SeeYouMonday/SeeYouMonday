import pandas as pd

df1 = pd.read_csv('data-scientist.csv')
df2 = pd.read_csv('software-engineer.csv')
df3 = pd.read_csv('computer-systems.csv')

frames = [df1, df2, df3]
result = pd.concat(frames)
result.drop_duplicates()
result.drop(result.columns[0], axis=1)

result.to_csv('out.csv', encoding='utf-8')
