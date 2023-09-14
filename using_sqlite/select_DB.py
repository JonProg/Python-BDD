import sqlite3
from main import DB_FILE, TABLE_ANIMES

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute(
    f'SELECT * FROM {TABLE_ANIMES} '
    'WHERE stars > 4.2'
)

row_one = cursor.fetchone()
print(row_one)

for row in cursor.fetchall():
    _id, name, stars = row
    print(_id, name, stars)

cursor.close()
connection.close()