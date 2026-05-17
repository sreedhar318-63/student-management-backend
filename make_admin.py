import sqlite3
import sys
import os

db_path = "kuppam.db"

def make_admin(username):
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"User '{username}' not found.")
            return
        
        if user[1] == 'admin':
            print(f"User '{username}' is already an admin.")
            return
            
        cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?", (username,))
        conn.commit()
        print(f"Successfully granted admin privileges to user '{username}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <username>")
    else:
        make_admin(sys.argv[1])
