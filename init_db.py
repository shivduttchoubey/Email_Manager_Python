import sqlite3

def initialize_database():
    """Ensures the database exists and has necessary tables."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT, 
                        email TEXT UNIQUE,
                        position TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender TEXT,
                        subject TEXT,
                        timestamp TEXT,
                        body TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS sync_info (
                        last_sync TEXT)''')
    
    conn.commit()
    conn.close()

initialize_database()
print("Database initialized successfully!")
