from database import get_connection

def add_order_history(order_id, comment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO order_history (order_id, comment) VALUES (%s, %s)",
        (order_id, comment)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_history_by_order(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM order_history WHERE order_id=%s ORDER BY created_at DESC",
        (order_id,)
    )
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history