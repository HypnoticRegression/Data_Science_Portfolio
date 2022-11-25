import sqlite3
import pandas as pd
import glob
import pathlib



method = 1 ## Select 1 for direct file path insert, 0 for batch file from folder insert

#Direct file insert path. Edit for direct file insert
dir_path=r'S:\Data\consumer_financial_complaints.csv'

#Glob method for iterating over batches of files for insertion
glob_path=r'S:\Data\*'
f = glob.glob(glob_path, recursive=True)


db = r'S:\Databases\main_db.db'
table = pathlib.PurePath(dir_path).stem


## Direct Insertion of single file
if method == 1:
    if pathlib.PurePath(dir_path).suffix == '.csv':
        df = pd.read_csv(dir_path)
    if pathlib.PurePath(dir_path).suffix == '.xlsx':
        df = pd.read_excel(dir_path)
    if pathlib.PurePath(dir_path).suffix == '.json':
        df = pd.read_json(dir_path)

    db = r'S:\Databases\main_db.db'
    table = pathlib.PurePath(dir_path).stem
    #Organize headers and remove any other unwanted symbols and replace with underscore
    print('Reformatting Column Headers...')
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(' ','_').str.replace('-','_')
    df.columns = df.columns.str.strip('?!.&^*()$#@')

    ########################
    #### Insert via SQL ####
    ########################

    #Print to let user know it started
    print("Starting Data Insert...")
    #Create connection to database
    try:
        conn = sqlite3.connect(db)
        df.to_sql(table, conn, if_exists="replace", index=False)
        print('Data Inserted into {}'.format(db))  
    except sqlite3.Error as ex:
                print (ex)
    finally:
        conn.close()
        print('Closing connection')




    #######################
    #### Query via SQL ####
    #######################
    def run_query(qry):
        #Print to let user know it started
        print("Starting query...")
        #Create connection to database
        try:
            conn = sqlite3.connect(db)  
        except sqlite3.Error as ex:
                    print (ex)
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
            print('Closing connection')




    sql_pull = run_query('''SELECT * FROM {} limit 10;'''.format(table))
    print(sql_pull)





##Iteration through file folder
if method == 0:
    for i in f:
        if pathlib.PurePath(i).suffix == '.csv':
            df = pd.read_csv(i)
        if pathlib.PurePath(i).suffix == '.xlsx':
            df = pd.read_excel(i)
        if pathlib.PurePath(i).suffix == '.json':
            df = pd.read_json(i)

        db = r'S:\Databases\main_db.db'
        table = pathlib.PurePath(i).stem
        #Organize headers and remove any other unwanted symbols and replace with underscore
        print('Reformatting Column Headers...')
        df.columns = map(str.lower, df.columns)
        df.columns = df.columns.str.replace(' ','_').str.replace('-','_')
        df.columns = df.columns.str.strip('?!.&^*()$#@')

        ########################
        #### Insert via SQL ####
        ########################

        #Print to let user know it started
        print("Starting Data Insert...")
        #Create connection to database
        try:
            conn = sqlite3.connect(db)
            df.to_sql(table, conn, if_exists="replace", index=False)
            print('Data Inserted into {}'.format(db))  
        except sqlite3.Error as ex:
                    print (ex)
        finally:
            conn.close()
            print('Closing connection')




        #######################
        #### Query via SQL ####
        #######################
        def run_query(qry):
            #Print to let user know it started
            print("Starting query...")
            #Create connection to database
            try:
                conn = sqlite3.connect(db)  
            except sqlite3.Error as ex:
                        print (ex)
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
                print('Closing connection')




        sql_pull = run_query('''SELECT * FROM {} limit 10;'''.format(table))
        print(sql_pull)
