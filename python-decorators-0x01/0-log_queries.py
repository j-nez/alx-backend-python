import sqlite3
from datetime import datetime

#### decorator to log SQL queries

def log_queries(func):
    
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        with open('queries.log', 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] Executing SQL query: {query}\n")
        return(func(*args, **kwargs))
    return wrapper




@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect(r"C:\Users\nyemi\Desktop\ALX_current\alx-backend-python\python-decorators-0x01\users.db")
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL)
""")
    cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)", ("alice", "alice@example.com"))
    cursor.execute(query)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query='SELECT *  FROM users')
print(users)

