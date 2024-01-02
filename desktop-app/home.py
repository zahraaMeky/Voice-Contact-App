import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from os import getcwd
import sqlite3
import gzip

def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

dir = resource_path("resources")
# def write_key():
#     global dir
#     key = Fernet.generate_key() # Generates the key
#     with open(dir +"/key.key", "wb") as key_file: # Opens the file the key is to be written to
#         key_file.write(key) 

# def load_key():
#     global dir
#     return open(dir + "/key.key", "rb").read()


# # write_key()

# key = load_key()
# print("key: ", key)

# f = Fernet(key)
# message = "WeAreTheBest".encode()
# encrypted_message = f.encrypt(message)
# print(encrypted_message)

def key_creation(password):
    kdf=PBKDF2HMAC(algorithm = hashes.SHA256(), salt=b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2', iterations=1024, length=32, backend=default_backend())
    key=Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
    return key

def encryption(b, password):
    f=key_creation(password)
    safe=f.encrypt(b)
    return safe

def decryption(safe, password):
    f=key_creation(password)
    b=f.decrypt(safe)
    return b

def open_cdb(name,password):
    global dir
    # f=gzip.open(getcwd()+name+'_crypted.sql.gz','rb')
    # f=gzip.open(dir + "/" + name + '_crypted.sql.gz','rb')
    f=gzip.open(name + '_crypted.sql.gz','rb')
    safe=f.read()
    f.close()
    content=decryption(safe,password)
    content=content.decode('utf-8')
    con=sqlite3.connect(':memory:')
    con.executescript(content)
    return con

def save_cdb(con,name,password):
    # fp=gzip.open(getcwd()+name+'_crypted.sql.gz','wb')
    # fp=gzip.open(dir + "/" + name + '_crypted.sql.gz','wb')
    fp=gzip.open(name + '_crypted.sql.gz','wb')
    b=b''
    for line in con.iterdump():
        b+=bytes('%s\n','utf8') % bytes(line,'utf8')
    b=encryption(b,password)
    fp.write(b)
    fp.close()


if __name__=='__main__':
    password=b'WeAreTheBest'
    name='VOICE_DB'
    # conn = sqlite3.connect(':memory:')
    
    # #conn.execute('CREATE TABLE PRODUCTS (ID INT PRIMARY KEY     NOT NULL,\nNAME           TEXT    NOT NULL,\nPRICE            REAL     NOT NULL,\nTAXES        REAL    NOT NULL);')
    # conn.execute('''
    #     CREATE TABLE IF NOT EXISTS rooms (
    #         id          INTEGER,
    #         name        TEXT,
    #         ip          TEXT    UNIQUE,
    #         description TEXT,
    #         PRIMARY KEY (
    #             id AUTOINCREMENT
    #         )
    #     );
    # ''')

    # # Insert data into the table
    # conn.execute("""CREATE TABLE IF NOT EXISTS users (
    #                         username TEXT NOT NULL UNIQUE,
    #                         password TEXT,
    #                         id       INTEGER UNIQUE,
    #                         role     INTEGER,
    #                         PRIMARY KEY (
    #                             id AUTOINCREMENT
    #                         )
    #                     );""")

    # conn.execute("""
    #                 INSERT INTO users (
    #                         username,
    #                         password,
    #                         id,
    #                         role
    #                     )
    #                     VALUES (
    #                         'admin',
    #                         'admin',
    #                         1,
    #                         1
    #                     );
    #                 """)

    # conn.execute("""INSERT INTO users (
    #                         username,
    #                         password,
    #                         id,
    #                         role
    #                     )
    #                     VALUES (
    #                         'user',
    #                         'user',
    #                         3,
    #                         0
    #                     );
    #                 """)


    # save_cdb(conn,name,password)
    # conn.close()
    
    conn = open_cdb(name,password)
    cursor = conn.execute('select * from users')
    headers = list(map(lambda x: x[0], cursor.description))
    print(headers)
    for x in cursor:
        for j in range(len(x)):
            print(headers[j]+' ',x[j])
        print('\n')
    
    # conn.execute("""
    #                 INSERT INTO users (
    #                         username,
    #                         password,
    #                         role
    #                     )
    #                     VALUES (
    #                         'root',
    #                         'IamROot',
    #                         1
    #                     );
    #                 """)
    
    # cursor = conn.execute('select * from users')
    # headers = list(map(lambda x: x[0], cursor.description))
    # print(headers)
    # for x in cursor:
    #     for j in range(len(x)):
    #         print(headers[j]+' ',x[j])
    #     print('\n')

    # save_cdb(conn,name,password)

    conn.close()