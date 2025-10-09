import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataBase:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('picapy.db')
            self.cursor = self.conn.cursor()
            
            logging.info("Database connection established.")
        except sqlite3.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def create_table(self):
        try: 
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE,
                    password TEXT NOT NULL
            )''')
            logging.info("Database connection established.")
        except sqlite3.Error as e:
            logging.error(f"Failed to create table: {e}")
            raise

 
    def insert_user(self, user, email, password):
        try: 
            self.cursor.execute('''
                INSERT INTO users (nome, email, password)
                VALUES (?, ?, ?)
                ''', 
                (user, email, password))
            logging.info("User inserted successfully.")
        except:
            logging.error("Failed to insert user.")
            raise

    
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed.")
        except sqlite3.Error as e:
            logging.error(f"Error closing connection: {e}")