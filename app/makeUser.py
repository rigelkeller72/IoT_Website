import sqlite3, secrets
from hashlib import md5


def checkName():
    print("aha")

def main():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    salty = secrets.token_hex(8)
    saltypass = password + salty
    storeword = md5(saltypass.encode('ascii')).hexdigest()
    conn = sqlite3.connect("servdb.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, salt) VALUES (?,?,?)",
                   (username,storeword,salty))
    conn.commit()
    cursor.close()
    conn.close()

main()