import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import db

def test_connection():
    try:
        db.connect()
        cursor = db.execute_sql('SELECT version();')
        version = cursor.fetchone()
        print(f"✅ Conectado correctamente a PostgreSQL: {version[0]}")
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
    finally:
        if not db.is_closed():
            db.close()

if __name__ == "__main__":
    test_connection()
