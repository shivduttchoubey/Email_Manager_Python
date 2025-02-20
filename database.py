import sqlite3

def initialize_database():
    """Creates necessary tables if they don't exist."""
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

def save_setting(key, value):
    """Saves a key-value setting to the database."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_setting(key):
    """Retrieves a setting value by key."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_member(name, email, position):
    """Adds a new member to the database."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO members (name, email, position) VALUES (?, ?, ?)", (name, email, position))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Member with this email already exists.")
    conn.close()

def get_members():
    """Fetches all members from the database."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, position FROM members")
    members = cursor.fetchall()
    conn.close()
    return members

def save_email(sender, subject, timestamp, body):
    """Stores received emails in the database."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emails (sender, subject, timestamp, body) VALUES (?, ?, ?, ?)", 
                   (sender, subject, timestamp, body))
    conn.commit()
    conn.close()

def get_emails():
    """Fetches stored emails."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sender, subject, timestamp, body FROM emails ORDER BY timestamp DESC")
    emails = cursor.fetchall()
    conn.close()
    return emails
