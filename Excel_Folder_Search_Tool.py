#Search Excel files and return row that contains value Python
import pandas as pd
import glob


keywords = 'Sunday','Friday'


matched_rows = pd.DataFrame() #Going to chuck all of our matches in here. Should generate new columns if it doesn't match 

path = '' #Put all files in one folder, and point path here
filepath = glob.glob(path + '/*.csv') #Make sure to change the file type if you switch to xlsx or csv


for file in filepath:
    df = pd.read_csv(file)
    df['filepath'] = file #Names the filed in a cell so we know which file the result was returned from and where to find it
    row_match = df.loc[df.isin(keywords).any(axis=1)]
    matched_rows = matched_rows.append(row_match, ignore_index = True) #Append the rows to our separate DF


matched_rows.head()


#matched_rows.to_csv('filepath') #enter filepath for export