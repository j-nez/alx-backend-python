import sqlite3
"""create a class based context manager to handle opening and closing database connections automatically"""
class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is not None:
                print("An error occurred:", exc_val)
            self.conn.close()

# Usage of the context manager
db_path = r"C:\Users\nyemi\Desktop\ALX_current\alx-backend-python\python-decorators-0x01\users.db"  # Update path if needed

with DatabaseConnection(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
print(results)
