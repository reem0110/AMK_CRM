from database import get_connection

def add_client(name, phone, address):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO clients (name, phone, address) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, phone, address))
        conn.commit()
        cursor.close()
        conn.close()

def get_all_clients():
    conn = get_connection()
    clients = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clients ORDER BY id DESC")
        clients = cursor.fetchall()
        cursor.close()
        conn.close()
    return clients

def search_clients(keyword):
    conn = get_connection()
    clients = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM clients WHERE name LIKE %s ORDER BY id DESC"
        cursor.execute(sql, (f"%{keyword}%",))
        clients = cursor.fetchall()
        cursor.close()
        conn.close()
    return clients

def delete_client(client_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = %s", (client_id,))
        conn.commit()
        cursor.close()
        conn.close()