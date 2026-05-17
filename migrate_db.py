import sqlite3
import os

db_path = "kuppam.db"

def migrate():
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'role' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user'")
            conn.commit()
            print("Successfully added 'role' column to 'users' table.")
        
        if 'email' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN email VARCHAR(100)")
            conn.commit()
            print("Successfully added 'email' column to 'users' table.")
        else:
            print("'role' and 'email' columns already exist.")
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
