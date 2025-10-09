import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('picapy.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE,
                password TEXT NOT NULL
        )''')

 
    def insert_user(self, user, email, password):
        self.cursor.execute('''
            INSERT INTO users (nome, email, password)
            VALUES (?, ?, ?)
            ''', 
            (user, email, password))

    
    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()