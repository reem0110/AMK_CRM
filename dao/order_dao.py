from database import get_connection

def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders")

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result