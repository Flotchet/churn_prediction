import pandas as pd
import sqlite3
import os

#to replace the pandas.read_csv() by pandas.read_sql()


def read_sql(sql_query : str, 
             database_path : str = "a_database_creation/database",
             database_name : str = "database.db") -> pd.DataFrame:
    """
    Read a database and return a dataframe
    
    Parameters
    ----------
    sql_query : str
        The sql query to read the database
    
    database_path : str, optional
        The path to the database, by default "a_database_creation/database"
    
    database_name : str, optional
        The name of the database, by default "database.db"
    
    Returns
    -------
    pandas.DataFrame
        The dataframe of the database

    Raises
    ------
    FileNotFoundError
        If the database is not found
    """
    database = os.path.join(database_path, database_name)

    if not os.path.exists(database):
        raise FileNotFoundError("The database is not found")

    conn = sqlite3.connect(database)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    
    return df



def modify_db_from_df(df : pd.DataFrame,
                      database_path : str = "a_database_creation/database",
                      database_name : str = "database.db",
                      table_name : str = "bank_churners") -> None:

    """
    Modify a database from a dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to modify the database

    database_path : str, optional
        The path to the database, by default "a_database_creation/database"

    database_name : str, optional
        The name of the database, by default "database.db"

    table_name : str, optional
        The name of the table to modify, by default "bank_churners"

    Raises
    ------
    FileNotFoundError
        If the database is not found

    ValueError
        If the database is the production database
    """

    if database == "poduction.db":
        raise ValueError("You are not allowed to access the production database")
    
    database = os.path.join(database_path, database_name)

    if not os.path.exists(database):
        raise FileNotFoundError("The database is not found")

    conn = sqlite3.connect(database)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    return None

if __name__ == "__main__":
    sql_query = "SELECT * FROM bank_churners"
    df = read_sql(sql_query)
    print(df.head())

    modify_db_from_df(df)