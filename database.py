import psycopg2
from authorisation import Checker
import os
from dotenv import load_dotenv
load_dotenv()



def connect():
    connection=psycopg2.connect(
        host="chatapp-db.cgryuk6swrq1.us-east-1.rds.amazonaws.com",
        port=5432,
        database="postgres",  # I had to change this name and put underscores because it has to made an environment variable for db container to access it and 
                                          # this double quotes cant be used there. 
                                          # Database_for_ChatApp i changed it later to connect it when rds initiates an database.
        user="postgres",
        password=os.getenv('DB_PASSWORD')
    )

    return connection


def create(connection):
    cur=connection.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS chatapp(id SERIAL PRIMARY KEY, username varchar, password BYTEA);")
    ## I added the IF NOT EXISTS after the docker so that i can call the create function every time.

    connection.commit()


def insert(connection, name, pasword):
    cur=connection.cursor()


    #!!Added later.
    if dupli_check(connection, name):
        cur.execute("INSERT INTO chatapp(username, password) VALUES (%s, %s)", (name, pasword))
    else:
        return "Username already exists. Opt a different username please."

    # added the dupli username checking function late so had to remove this line.
    #cur.execute("INSERT INTO chatapp(username, password) VALUES (%s, %s)", (name, pasword))

    connection.commit()


def dupli_check(connection, username):

    cur=connection.cursor()

    cur.execute("SELECT * FROM chatapp WHERE username = %s", (username,))

    data=cur.fetchone()

    if data is None:
        return True
    else:
        return False
    


def find(connection, name, pasword):
    
    cur=connection.cursor()

    cur.execute("SELECT * FROM chatapp WHERE username = %s", (name,))
    data=cur.fetchone()
    if data is None:
        return "NO DATA FOUND"
    else:
        hashed=bytes(data[2])
    
    if Checker(pasword, hashed):
        return data
    else:
        return "NO DATA FOUND"
    
