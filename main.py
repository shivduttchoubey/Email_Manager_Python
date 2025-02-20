import os
import sqlite3
from ui import EmailManagerUI
from setup import setup_application
from email_handler import check_new_emails
from totp_auth import verify_totp

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

def main():
    """Main function to control the email manager flow."""
    initialize_database()
    
    # Check if setup is required
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key='setup_done'")
    setup_done = cursor.fetchone()
    conn.close()
    
    if not setup_done:
        setup_application()  # Runs first-time setup
    
    # Verify user via TOTP
    if not verify_totp():
        print("TOTP verification failed. Exiting application.")
        return
    
    # Check for new emails before launching UI
    check_new_emails()
    
    # Launch GUI
    app = EmailManagerUI()
    app.run()
    
if __name__ == "__main__":
    main()
