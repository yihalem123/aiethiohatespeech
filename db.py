import sqlite3

connection = sqlite3.connect('./db/database.db')

with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO admins ( email,password) VALUES (?, ?)",
            ( 'yihalemmande123@aiethiopia.com','yihalem')
            )


connection.commit()
connection.close()