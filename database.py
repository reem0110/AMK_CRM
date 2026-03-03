import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='probroyoyo2020',  # change if needed
            database='crm_amk'
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None