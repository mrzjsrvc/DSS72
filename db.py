
from __future__ import print_function
import mysql.connector
import json
import pandas as pd
from sqlalchemy import create_engine

home_path = "./"
init_script_path = home_path+"init.sql"
suffix = ".txt"
csv_names = ["customers","vehicles","times"]

host = "localhost"
port = "3306"
user = "root"
password = ""
database = "deliverydb"

engine = create_engine('mysql+mysqlconnector://'+user+':'+password+'@'+host+':'+port+'/'+database, echo=False)

# DO NOT ADD INSERTS IN THE INIT-SCRIPT, IT CAN'T PARSE THEM HERE(yet), use "run_sql_string(str)" instead
def run_init_script(init_path=init_script_path):
    buffer = ""
    insert_bool = False
    for line in open(init_path, "r", encoding='utf-8'):
        buffer += line
        if line[0:6] == "INSERT":
            insert_bool = True
        if line[-2] == ";":
            if insert_bool is True:
                # DO STUFF
                insert_bool = False
            else:
                engine.execute(buffer)

            print(buffer)
            buffer = ""

# Each txt-file must have the labels/column names ontop, and the file names should be listed in the variables at the top
def load_csvs_into_database(directory=home_path,file_names=csv_names,extensions=suffix):
    for i in file_names:
        df = pd.read_csv(directory+i+extensions)
        contents = df.to_sql(con=engine, name=i, if_exists='replace')

def clean_data(to_clean):
    cleaned_data = []
    for i in to_clean:
        cleaned_data.append(i[0:4])
    return cleaned_data

# This runs all SQL queries(both get & set)
def run_sql_string(str):
    try:
        return (engine.execute(str)).fetchall()
        # return clean_data((engine.execute(str)).fetchall())
        # return json.dumps(clean_data((engine.execute(str)).fetchall()))
    except:
        return "Done"

run_init_script()
load_csvs_into_database()
print(" === USE THE COMMAND run_sql_string(sql_query) TO INTERACT WITH THE DATABASE ===")
