import psycopg2
from authorisation import Checker
import os
from dotenv import load_dotenv
load_dotenv()



def connect():
    connection=psycopg2.connect(
        host="localhost",
        port=5432,
        database="Database for ChatApp",
        user="postgres",
        password=os.getenv('DB_PASSWORD')
    )

    return connection


def create(connection):
    cur=connection.cursor()

    cur.execute("CREATE TABLE chatapp(id SERIAL PRIMARY KEY, username varchar, password BYTEA);")

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
    
