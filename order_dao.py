from database import get_connection
from models import Order

def get_all_orders():
    conn = get_connection()
    orders = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders")
        for row in cursor.fetchall():
            orders.append(Order(**row))
        cursor.close()
        conn.close()
    return orders