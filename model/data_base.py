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

   
    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, user_name, email FROM users")
        rows = cursor.fetchall()
        # Converte para lista de dicionários
        return [
            {"id": row[0], "user_name": row[1], "email": row[2]}
            for row in rows
        ]

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("Database connection closed.")
        except sqlite3.Error as e:
            logging.error(f"Error closing connection: {e}")
    
    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, user_name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "user_name": row[1],
                "email": row[2]
            }
        return None
    

    def update_user(self, user_id, user_name=None, email=None, password=None):
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
        Remove um usuário pelo ID.
        Retorna True se o usuário existia e foi removido, False caso contrário.
        """
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0