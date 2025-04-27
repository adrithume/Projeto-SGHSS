from db import get_connection

def test_db_service():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    return cursor.fetchone()