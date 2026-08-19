import mysql.connector
from config import *

def drop_n_create_database(Database_name):
    # conn = mysql.connector.connect(user='root', password='password', host='localhost')
    # database_config = {'user': 'root', 'password': 'password', 'host': 'localhost'}
    conn = mysql.connector.connection.MySQLConnection(**database_config)
    
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {Database_name};")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {Database_name};")
    conn.commit()
    cur.close()
    conn.close()
    print('Database created successfully')
    
def create_customer_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE CUSTOMER (
                    `ID`                INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `NAME`              VARCHAR(100) NOT NULL,
                    `EMAIL`             VARCHAR(150),
                    `PHONE`             VARCHAR(13),
                    `ADDRESS`           TEXT,
                    `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )AUTO_INCREMENT=100;""")
    conn.commit()
    cur.close()
    conn.close()
    print('table customer created successfully')
    
def create_product_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE PRODUCT (
                    `ID`                INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `NAME`              VARCHAR(100) NOT NULL,
                    `DESCRIPTION`       VARCHAR(150),
                    `PRICE`             DOUBLE NOT NULL,
                    `INVENTORY`         MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,
                    `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )AUTO_INCREMENT=1000;""")
    conn.commit()
    cur.close()
    conn.close()
    print('table product created successfully')
    
    
def create_sale_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE SALE (
                    `ID`                INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    `CUST_ID`           INT UNSIGNED,
                    `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (CUST_ID) REFERENCES CUSTOMER(ID)
                )AUTO_INCREMENT=10000;""")
    conn.commit()
    cur.close()
    conn.close()
    print('table sale created successfully')

def create_sale_row_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE SALE_ROW (
                    `SALE_ID`           INT UNSIGNED,
                    `PRODUCT_ID`        INT UNSIGNED,
                    `QUANTITY`          MEDIUMINT UNSIGNED,
                    `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (SALE_ID, PRODUCT_ID),
                    FOREIGN KEY (SALE_ID) REFERENCES SALE(ID),
                    FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT(ID)
                )AUTO_INCREMENT=10000;""")
    conn.commit()
    cur.close()
    conn.close()
    print('table sale_row created successfully')
    
if __name__ == '__main__':
    drop_n_create_database(database_name)
    create_customer_table()
    create_product_table()
    create_sale_table()
    create_sale_row_table()