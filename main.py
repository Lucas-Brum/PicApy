import sqlite3

user = 'Lucas'
email = 'lucasbrum@gmail.com'
password = '123456'

conn = sqlite3.connect('picapy.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        password TEXT NOT NULL
)''')

cursor.execute('''
INSERT INTO users (nome, email, password)
VALUES (?, ?, ?)
''', (user, email, password))

conn.commit()

cursor.close()
conn.close()
