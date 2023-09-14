import pymysql
import pymysql.cursors 
import dotenv
import os

TABLE_NAME = 'customers'

CURRENT_CURSOR = pymysql.cursors.SSDictCursor 
#Usado quando temos uma grande quantidade de dados e precisamos de uma otimização
#Não da para usar o cursor.scroll() por conta que só a linha atual é salva na mémoria

dotenv.load_dotenv()
#--------- --------- --------- CONNECTION WITH SERVER --------- --------- --------- 
connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    charset='utf8mb4',
    cursorclass = CURRENT_CURSOR, 
)
#--------- --------- --------- --------- --------- --------- --------- --------- 
#É ideal que você faça somente uma connection com o servidor pois será menos custoso
with connection:
    with connection.cursor() as cursor:
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} ('
            'id INT NOT NULL AUTO_INCREMENT, '
            'nome VARCHAR(50) NOT NULL, '
            'idade INT NOT NULL, '
            'PRIMARY KEY(id) '
            ') '
        )
        #cuidado com isso, ele limpa toda a tabela !!
        cursor.execute(f'TRUNCATE TABLE {TABLE_NAME}')

    connection.commit()
#--------- --------- --------- --------- --------- --------- --------- --------- 
    #inserindo somente um valor
    with connection.cursor() as cursor:
        sql = (
            f'INSERT INTO {TABLE_NAME} '
            '(nome, idade) VALUES (%s, %s)'
        )
        cursor.execute(sql, ("Jonas", 17))
    connection.commit()
#--------- --------- --------- --------- --------- --------- --------- --------- 
    #inserir vários valores
    with connection.cursor() as cursor:
        sql = (
            f'INSERT INTO {TABLE_NAME} '
            '(nome, idade) VALUES (%(nome)s, %(idade)s)'
        )
        data = (
            {"nome":"Samuel", "idade":21},
            {"nome":"Dandara", "idade":1},
            {"nome":"Lany", "idade":20},
        )
        cursor.executemany(sql, data)
    connection.commit()
#--------- --------- --------- --------- --------- --------- --------- --------- 
    # Lendo os valores com SELECT
    #Sempre colocar defesas contra sqlinjection exemplos: limitar caracteres, cashing, proibir valores como ;,/
    with connection.cursor() as cursor:
        menor_id = int(input('Digite o menor id: ')) 
        maior_id = int(input('Digite o maior id: '))

        sql = (
            f'SELECT * FROM {TABLE_NAME} '
            'WHERE id BETWEEN %s AND %s  '
        )
        cursor.execute(sql, (menor_id, maior_id)) 
        print(cursor.mogrify(sql, (menor_id, maior_id)))  

        data5 = cursor.fetchall()
        for row in data5:
            print(row)
        print()
#--------- --------- --------- --------- --------- --------- --------- ---------
    #Deletando valores
    with connection.cursor() as cursor:
        sql = (
            f'DELETE FROM {TABLE_NAME} '
            'WHERE id = 2'
        )
        cursor.execute(sql)
        connection.commit()

        cursor.execute(f'select * from {TABLE_NAME}') 
        data6 = cursor.fetchall()
        #for row in data6:
            #print(row)

#--------- --------- --------- --------- --------- --------- --------- ---------
    #Editando com UPDATE, WHERE e placeholders no PyMySQL
    with connection.cursor() as cursor:
        sql = (
            f'UPDATE {TABLE_NAME} '
            'SET nome=%s, idade=%s '
            'WHERE id=%s'
        )
        cursor.execute(sql, ('Eleonor', 102, 4))  
        cursor.execute(f'SELECT * FROM {TABLE_NAME} ')  

        #cursor.scroll(1, 'absolute')
        #Usado para deslocar a posição do ponteiro sem presisar criar uma variavel
        for row in cursor.fetchall(): 
            print(row)

    connection.commit()

    