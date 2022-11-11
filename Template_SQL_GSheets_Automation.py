#Import needed packages
import pandas as pd
import pyodbc
import pygsheets
from datetime import datetime,timedelta
import numpy as np


##Import for initializing GSheets for the first time
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError



pickle_path = 'path to client secret'
#Authorize gsheets access
#You'll need to switch out this filepath
gc = pygsheets.authorize(client_secret='gmail_cs.json',credentials_directory=pickle_path)
#Open g sheets workbook. We'll be calling the worksheets later
workbook_key = 'workbook key'
workbook = gc.open_by_key(workbook_key)





#######################
#### Query via SQL ####
#######################

def run_query(qry):
    #Print to let user know it started
    print("Starting query...")
    #Creat connection
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=Server;'
                        'Database=DB;'
                        'Trusted_Connection=yes;')
    #Execute Query + Error handling
    try:
        output = pd.read_sql(qry,conn)
        print("Ran successfully!")
        return(output)
    except Exception as inst:
            print("WARNING: an error has occurred. Error type: "+str(type(inst)))
            print("An error has occurred. Please manually review.")
    finally:
      conn.close()



sql_data=run_query('''

SQL Query Here

''')




print('Uploading Data to G-Sheets...')

#Get datetime and find week ending and week beginning
day = datetime.now().strftime('%m/%d/%Y')
dt = datetime.strptime(day, '%m/%d/%Y')
start = dt - timedelta(days=dt.isoweekday())
start = start.date() #Week start date in case that is the relevant date to be called
end = start + timedelta(days=6)
worksheet_title = 'W/E {end} Data'.format(end = end)


#Read in and copy data
spreadsheet_insert = sql_data.copy()


#Add new worksheet and title accordingly to insert data into tab
workbook.add_worksheet(worksheet_title,rows = 5000)
worksheet = workbook.worksheet_by_title(worksheet_title)
worksheet.set_dataframe(spreadsheet_insert, start=(1,1),nan='')


##Sets Vertical/Horizontal Alignment and Text Wrap for cells
model_cell = worksheet.cell('A2')
model_cell.set_vertical_alignment(pygsheets.custom_types.VerticalAlignment.MIDDLE).set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER).wrap_strategy = 'WRAP'
rng = worksheet.get_values('A2', 'G4000', returnas='range')
rng.apply_format(model_cell)


#Refines Text Column formatting
comments_model_cell = worksheet.cell('H2') #We want these aligned default left, so we have to use different formatting for them
comments_model_cell.set_vertical_alignment(pygsheets.custom_types.VerticalAlignment.MIDDLE).wrap_strategy = 'WRAP'
rng2 = worksheet.get_values('H2', 'I4000', returnas='range') #Comments Range
rng2.apply_format(comments_model_cell)


#Header Formatting
header_model = worksheet.cell('A1')
header_model.set_vertical_alignment(pygsheets.custom_types.VerticalAlignment.MIDDLE).set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER).set_text_format('bold',True).wrap_strategy = 'WRAP'
rng3 = worksheet.get_values('A1', 'I1', returnas='range')
rng3.apply_format(header_model)


#Set appropriate column widths
worksheet.adjust_column_width(1,7, pixel_size = 150)
worksheet.adjust_column_width(8,9, pixel_size = 500)


worksheet.sort_range(sortorder='DESCENDING',start=(2,1),end=(5000,16)) #If any sorting of the worksheet is needed

# #Refresh Update time
dt=workbook.worksheet_by_title('Last Updated')
dt.update_value('B1',datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# Email the workbook to yourself to ensure that it ran, or email to the appropriate stakeholder
workbook.share('email@address.com', role='writer', type='user', emailMessage='The Weekly SQL Automation has completed successfully.')
print('Complete.')