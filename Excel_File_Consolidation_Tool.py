#Search Excel files and return row that contains value Python
import pandas as pd
import glob

matched_rows = pd.DataFrame() #Going to chuck all of our matches in here. Should generate new columns if it doesn't match 

path = '' #Put all files in one folder, and point path here
filepath = glob.glob(path + '/*.csv') #Make sure to change the file type if you switch to xlsx or csv


final_file = pd.DataFrame()
for file in filepath:
    df = pd.read_csv(file)
    #df['filepath'] = file #Names the filed in a cell so we know which file the result was returned from and where to find it
    final_file = final_file.append(df, ignore_index = True) #Append the rows to our final DF


final_file.head()


final_file.to_csv('filepath',index= False) #enter filepath for export