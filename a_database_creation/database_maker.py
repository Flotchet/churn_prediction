#create a database from  a csv file
import sqlite3
import pandas
import os
import warnings

#import for making a NoSQL database
import pymongo
from pymongo import MongoClient

def create_database(csv_file : str = "a_database_creation/data/BankChurners.csv", 
                    database_path : str = "a_database_creation/database",
                    database_name : str = "database.db",
                    warn : bool = True) -> None:
    """
    Create a database from a csv file

    Parameters
    ----------
    csv_file : str, optional
        The path to the csv file, by default "a_database_creation/data/BankChurners.csv"

    database_path : str, optional
        The path to the database, by default "a_database_creation/database"

    database_name : str, optional
        The name of the database, by default "database.db"

    warn : bool, optional
        If True, a warning is raised if the csv file is not found or if there is 
        already a database with the same name at the path
        , by default True

    raise
    -----
    FileNotFoundError
        If the csv file is not found

    Warnings
    --------
    UserWarning
        If the database already exists, it is deleted and recreated
    """

    if not os.path.exists(csv_file):
        if warn:
            warnings.warn("The csv file is not found")
        raise FileNotFoundError("The csv file is not found")

    if not os.path.exists(database_path):
        os.mkdir(database_path)

    database = os.path.join(database_path, database_name)

    if os.path.exists(database):
        if warn:
            warnings.warn("The database already exists, it is deleted and recreated")
        os.remove(database)

    conn = sqlite3.connect(database)

    df = pandas.read_csv(csv_file)

    df.to_sql("bank_churners", conn, if_exists="replace", index=False)

    #make a table USER with two column ID, Password, Password_key
    #ID is the primary key
    #Password is a string
    #Password_key is a string
    #ID is an integer
    #ID is autoincremented
    conn.execute("""CREATE TABLE USER (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Password TEXT NOT NULL,
                    Password_key TEXT NOT NULL
                    );""")

    #create a COMMENTS table with ID, USER_ID, Result, Comments 
    #ID is the primary key
    #USER_ID is a foreign key
    #Result is a string
    #Comments is a string
    conn.execute("""CREATE TABLE COMMENTS (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    USER_ID INTEGER NOT NULL,
                    Result TEXT NOT NULL,
                    Comments TEXT NOT NULL,
                    FOREIGN KEY(USER_ID) REFERENCES USER(ID)
                    );""")

    conn.close()

    return None


if __name__ == "__main__":
    create_database()