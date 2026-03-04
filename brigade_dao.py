from database import get_connection

def add_brigade(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO brigades (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_brigades():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM brigades")
    brigades = cursor.fetchall()
    cursor.close()
    conn.close()
    return brigades

def delete_brigade(brigade_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM brigades WHERE id=%s", (brigade_id,))
    conn.commit()
    cursor.close()
    conn.close()