import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='PONajith#2005',
        database='uzhavan_db'
    )
