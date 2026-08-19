import mysql.connector
from config import *
    
def get_customer_data(ID):
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database)
    cur = conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM CUSTOMER WHERE ID=%s LIMIT 1;"
    cur.execute(SQL_QUERY, (ID,))
    # result = cur.fetchall()
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

if __name__ == "__main__":
    data = get_customer_data(100)
    print(f'data for customer ID=100: {data}')