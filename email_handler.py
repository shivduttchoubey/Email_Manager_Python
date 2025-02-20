import smtplib
import imaplib
import email
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_email_credentials():
    """Fetch stored email credentials from the database."""
    conn = sqlite3.connect("email_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key='email' OR key='password'")
    creds = cursor.fetchall()
    conn.close()
    return creds[0][0], creds[1][0] if creds else (None, None)

def send_email(recipient, subject, body):
    """Send an email using stored SMTP credentials."""
    sender_email, sender_password = get_email_credentials()
    if not sender_email or not sender_password:
        print("Email credentials not found. Please run setup.")
        return False
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def check_new_emails():
    """Fetch new emails via IMAP and store them in the database."""
    sender_email, sender_password = get_email_credentials()
    if not sender_email or not sender_password:
        print("Email credentials not found. Please run setup.")
        return
    
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(sender_email, sender_password)
        mail.select('inbox')
        
        result, data = mail.search(None, 'UNSEEN')
        email_ids = data[0].split()
        
        for email_id in email_ids:
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    sender = msg['From']
                    subject = msg['Subject']
                    timestamp = msg['Date']
                    body = ""
                    
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    conn = sqlite3.connect("email_manager.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO emails (sender, subject, timestamp, body) VALUES (?, ?, ?, ?)", 
                                   (sender, subject, timestamp, body))
                    conn.commit()
                    conn.close()
        
        mail.logout()
    except Exception as e:
        print(f"Failed to check new emails: {e}")