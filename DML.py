import mysql.connector
from config import *
    
def insert_customer_data(NAME, EMAIL=None, PHONE=None, ADDRESS=None):
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database)
    cur = conn.cursor()
    SQL_QUERY = "INSERT INTO CUSTOMER (NAME, EMAIL, PHONE, ADDRESS) VALUES (%s, %s, %s, %s);"
    cur.execute(SQL_QUERY, (NAME, EMAIL, PHONE, ADDRESS))
    conn.commit()
    user_id = cur.lastrowid
    cur.close()
    conn.close()
    print(f'user data inserted successfully with id: {user_id}')
    return user_id
    

if __name__ == "__main__":
    insert_customer_data('jafar')