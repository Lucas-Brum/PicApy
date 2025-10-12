import sqlite3
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataBase:
    def __init__(self):
        db_path = Path("db/picapy.db")

        db_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.conn = sqlite3.connect(str(db_path))
            self.cursor = self.conn.cursor()
            logging.info("Database connection established.")
        except sqlite3.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def create_table(self):
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,         
                    email TEXT UNIQUE,
                    password TEXT NOT NULL
                )
                """
            )
            self.conn.commit()
            logging.info("Users table created or already exists.")
        except sqlite3.Error as e:
            logging.error(f"Failed to create table: {e}")
            raise

    def insert_user(self, user_name, email, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (user_name, email, password) VALUES (?, ?, ?)",
                (user_name, email, password),
            )
            self.conn.commit()
            logging.info("User inserted successfully.")
            return {
                "success": True,
                "user": {
                    "id": self.cursor.lastrowid,
                    "user_name": user_name,
                    "email": email,
                },
            }
        except sqlite3.IntegrityError as e:
            if "email" in str(e).lower() and "unique" in str(e).lower():
                logging.warning(f"Email '{email}' already exists.")
                return {"success": False, "error": "Email already registered."}
            else:
                logging.error(f"Integrity error: {e}")
                return {"success": False, "error": "Failed to save user to database."}
        except Exception as e:
            logging.error(f"Database error: {e}")
            return {"success": False, "error": "Failed to save user to database."}

    def show_users(self):
        try:
            self.cursor.execute("SELECT id, user_name, email, password FROM users")
            rows = self.cursor.fetchall()

            if rows:
                logging.info("Users found in database: picapy.db")
                for row in rows:
                    print(
                        f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Password: {row[3]}"
                    )
            else:
                logging.info("No users found in database.")
        except Exception as e:
            logging.error(f"Failed to fetch users: {e}")
            raise

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed.")
        except sqlite3.Error as e:
            logging.error(f"Error closing connection: {e}")
