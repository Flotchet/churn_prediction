import sqlite3
from cryptography.fernet import Fernet

def password_encryptor(user_id : int, password_to_encrypt : str, database : str) -> str:
    """
    Encrypt the password of a user

    Parameters
    ----------
    user_id : int
        The id of the user

    password_to_encrypt : str
        The password to encrypt

    database : str
        The path to the database

    Returns
    -------
    str
        The encrypted password's key to decrypt
    """
    #make a key
    key = Fernet.generate_key()
    #make a fernet object
    f = Fernet(key)
    #encrypt the password
    encrypted_password = f.encrypt(password_to_encrypt.encode())
    #add the encrypted password and the key to the database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("UPDATE USER SET Password = ?, Password_key = ? WHERE ID = ?", (encrypted_password, key, user_id))
    conn.commit()
    conn.close()
    #return the key
    return key

def password_and_user_checker(user_id : int, password : str, database : str) -> bool:
    """
    Check if the user is in the database and if the password is correct

    Parameters
    ----------
    user_id : int
        The id of the user

    password : str
        The password to check

    database : str
        The path to the database

    Returns
    -------
    bool
        True if the user is in the database and if the password is correct
    """
    #check if the user is in the database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE ID = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    #if the user is not in the database, return False
    if user is None:
        return False
    #if the user is in the database, check if the password is correct

    key = user[2]
    #make a fernet object
    f = Fernet(key)
    #decrypt the password
    decrypted_password = f.decrypt(user[1])
    #check if the password is correct
    if password == decrypted_password.decode():
        return True

    return False

