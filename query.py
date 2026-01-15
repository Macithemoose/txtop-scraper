import pandas as pd
import numpy as np

# comparing two files: 
# 1. enter the path to the earlier file you'd like to compare, and to the new file. Side note: need to name the file with ONLY new scrapes
# and store it separately, so that in the future we can make a comparison with the latest WHOLE file. 
# 2. Check whether each file is an excel file or a csv file; this will allow me to determine dataframe conversion
# 3. Do a comparison between left and right; take only FROM RIGHT which ISN'T IN LEFT.

def extract_new_only(first_file_path, second_file_path):
    if first_file_path.endswith('.csv'):
        df1 = pd.read_csv(first_file_path)
    else:
        df1 = pd.read_excel(first_file_path)

    if second_file_path.endswith('.csv'):
        df2 = pd.read_csv(second_file_path)
    else:
        df2 = pd.read_excel(second_file_path)
    
    new_df = pd.DataFrame(columns = df2.columns)

    for entry in range(len(df2['tail number'])):
        # print(df2['tail number'][entry])
        if df2['tail number'][entry] not in df1['tail number']:
            new_df.loc[entry] = df2.loc[entry]
    
    print(df1['tail number'])


extract_new_only('C:/Users/macik/txtop-scraper/data/Beechcraft V35B Bonanza_20-05-2025.xlsx - Sheet.csv', 'data/Beechcraft V35B Bonanza_12-06-2025.csv')