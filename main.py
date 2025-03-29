import pandas as pd
'''
Create amazing plots in this file. You will read the data from `data_organized` 
(unless your raw data required no reduction, in which case you can read your data from `raw_data`). 
You will do plot-related work such as joins, column filtering, pivots, 
small calculations and other simple organizational work. 
'''

df = pd.read_csv('raw_data\data_by_genres.csv')
print(len(df))