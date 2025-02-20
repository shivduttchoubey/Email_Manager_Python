import pyotp
import qrcode
import sqlite3

def initialize_totp():
    """Generates and stores a TOTP secret, returning the QR code for scanning."""
    secret = pyotp.random_base32()
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS totp (secret TEXT)")
    cursor.execute("DELETE FROM totp")  # Ensures only one secret exists
    cursor.execute("INSERT INTO totp (secret) VALUES (?)", (secret,))
    conn.commit()
    conn.close()
    
    uri = pyotp.totp.TOTP(secret).provisioning_uri("EmailManager", issuer_name="Org")
    qr = qrcode.make(uri)
    qr.show()
    print("Scan the QR code with your authenticator app.")

def verify_totp(user_code):
    """Verifies a user-entered TOTP code."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT secret FROM totp")
    secret = cursor.fetchone()
    conn.close()
    
    if not secret:
        print("TOTP not set up.")
        return False
    
    totp = pyotp.TOTP(secret[0])
    return totp.verify(user_code)
