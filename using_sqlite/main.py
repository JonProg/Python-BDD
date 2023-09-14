import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).parent
DB_NAME = 'db.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME
TABLE_ANIMES = 'animes'

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# CUIDADO: fazendo delete sem where
cursor.execute(
    f'DELETE FROM {TABLE_ANIMES}'
)
cursor.execute(
    f'DELETE FROM sqlite_sequence WHERE name="{TABLE_ANIMES}"'
)
connection.commit()

cursor.execute(
    f'CREATE TABLE IF NOT EXISTS {TABLE_ANIMES}'
    '('
    'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    'name TEXT,'
    'stars REAL'
    ')'
)
connection.commit()

#CUIDADO: sql injection que é quando os dados seram prenchidos pelo o usuario
#ele pode passar comandos para a base de dados por exemplo: delete from tabela

sql = (
    f'INSERT INTO {TABLE_ANIMES} (name , stars)'
    'VALUES (:name, :stars)'
)

#Usando dicionarios na entrada dos dados -- VALUES (:name, :stars)
cursor.executemany(sql,(
    {'name':'Vou ser Apagado', 'stars':0},
    {'name':'Naruto', 'stars':4.7},
    {'name':'Dragon Ball', 'stars':4.6},
    {'name':'Hellsing', 'stars':4.4},
    {'name':'One Punch', 'stars':4.2},
    {'name':'One Piece', 'stars':4.8},
))

#Usando tuplas na entrada -- VALUES (?,?)
#cursor.executemany(sql, (('Naruto', 4.7), ('Dragon Ball', 4.6)))

#Fazendo dessa forma evitamos o sql injection
#já que agora estamos fazendo uma separação entre
#codigo sql e valores.

connection.commit()

if __name__ == '__main__':

    cursor.execute(
        f'UPDATE {TABLE_ANIMES} '
        'SET name = "Inazuma Eleven", stars = 4.5 '
        'WHERE id = 1'
    )
    connection.commit()
    
    cursor.execute(
    f'SELECT * FROM {TABLE_ANIMES} '
    )

    for row in cursor.fetchall():
        _id, name, stars = row
        print(_id, name, stars)

    cursor.close()
    connection.close()
