import sqlite3
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class DataBase:
    """
    Handles SQLite database connections and user-related operations.
    Provides methods to create tables, insert, update, delete, and fetch users.
    """

    def __init__(self)-> None:
        """
        Initializes the database connection and ensures the database file exists.
        """
        db_path = Path("db/picapy.db")
        db_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.conn = sqlite3.connect(str(db_path))
            self.cursor = self.conn.cursor()
            logging.info("Database connection established.")
        except sqlite3.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def create_table(self) -> None:
        """
        Creates the 'users' table if it does not already exist.
        """
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

    def insert_user(self, user_name:str, email:str, password:str) -> dict:
        """
        Inserts a new user into the database.

        Args:
            user_name (str): The name of the user.
            email (str): The user's email (must be unique).
            password (str): The user's password.

        Returns:
            dict: Success status and user data or an error message.
        """
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

    def get_all_users(self) -> list[dict]:
        """
        Retrieves all users from the database.

        Returns:
            list: A list of dictionaries with user details.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, user_name, email FROM users")
        rows = cursor.fetchall()
        return [
            {"id": row[0], "user_name": row[1], "email": row[2]}
            for row in rows
        ]

    def get_user_by_id(self, user_id:int) -> dict | None:
        """
        Retrieves a single user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict or None: User data if found, else None.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, user_name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "user_name": row[1], "email": row[2]}
        return None

    def update_user(self, user_id:int, user_name:str, email:str, password:str) -> dict:
        """
        Updates an existing user's information.

        Args:
            user_id (int): The ID of the user to update.
            user_name (str, optional): New name for the user.
            email (str, optional): New email (must be unique).
            password (str, optional): New password.

        Returns:
            dict: Success status and updated user data, or an error message.
        """
        current = self.get_user_by_id(user_id)
        if current is None:
            return {"success": False, "error": "User not found"}

        if email is not None and email != current["email"]:
            self.cursor.execute("SELECT 1 FROM users WHERE email = ? AND id != ?", (email, user_id))
            if self.cursor.fetchone():
                return {"success": False, "error": "Email already in use"}

        fields = []
        values = []
        if user_name is not None:
            fields.append("user_name = ?")
            values.append(user_name)
        if email is not None:
            fields.append("email = ?")
            values.append(email)
        if password is not None:
            fields.append("password = ?")
            values.append(password)

        if not fields:
            return {"success": True, "user": current}

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

        updated = self.get_user_by_id(user_id)
        return {"success": True, "user": updated}

    def delete_by_id(self, user_id: int) -> bool:
        """
        Deletes a user by ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the user existed and was deleted, False otherwise.
        """
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close(self) -> None:
        """
        Closes the database connection safely.
        """
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed.")
        except sqlite3.Error as e:
            logging.error(f"Error closing connection: {e}")
