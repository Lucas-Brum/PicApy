import sqlite3

from db import DataBase
from security import Security

user = 'Lucas'
email = 'lucasbrum@gmail.com'
password = Security.hash_password("minhasenha123")

db = DataBase()
db.create_table()
db.insert_user(user, email, password)
db.show_users()
db.close()


