from database import get_connection

def add_client(name, phone, address):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO clients (name, phone, address) VALUES (%s,%s,%s)",
        (name, phone, address)
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_all_clients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clients ORDER BY id DESC")

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def search_clients(keyword):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM clients WHERE name LIKE %s",
        (f"%{keyword}%",)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def delete_client(client_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clients WHERE id=%s", (client_id,))

    conn.commit()
    cursor.close()
    conn.close()