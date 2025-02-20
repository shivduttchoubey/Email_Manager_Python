import tkinter as tk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Email configuration
    sender_email = "shivduttchoubey@gmail.com"
    sender_password = ""
    receiver_email = "shivduttchoubey123@gmail.com"
    subject = "Test Email from Python"
    body = "This is a test email sent from a Python script."

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Create a secure SSL context
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        # Login to the email server
        server.login(sender_email, sender_password)
        
        # Send the email
        server.send_message(message)
        
        # Close the connection
        server.quit()
        
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Email Sender")
root.geometry("300x150")

# Create and pack a button
send_button = tk.Button(root, text="Send Email", command=send_email)
send_button.pack(expand=True)

# Start the GUI event loop
root.mainloop()