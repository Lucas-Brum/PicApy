import sqlite3

from db import DataBase

user = 'Lucas'
email = 'lucasbrum@gmail.com'
password = '123456'

db = DataBase()
db.create_table()
db.insert_user(user, email, password)
db.close()


