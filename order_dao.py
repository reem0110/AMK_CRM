from database import get_connection
from models import Order
from order_history_dao import add_order_history

def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def assign_brigade_to_order(order_id, brigade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET brigade_id = %s WHERE id = %s",
        (brigade_id, order_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    # Optional: add an order history entry
    add_order_history(order_id, f"Brigade {brigade_id} assigned")
    
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