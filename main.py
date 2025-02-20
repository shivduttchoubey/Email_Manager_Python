import database
import totp_auth
import gui
import tkinter as tk
from tkinter import simpledialog, messagebox

def prompt_credentials():
    """Prompt user for email credentials in a Tkinter dialog."""
    root = tk.Tk()
    root.withdraw()
    email = simpledialog.askstring("Setup", "Enter your email:")
    password = simpledialog.askstring("Setup", "Enter your password:", show='*')
    
    if email and password:
        database.save_setting("email", email)
        database.save_setting("password", password)
    else:
        messagebox.showerror("Error", "Email and password are required.")
        exit()

def main():
    """Main function to initialize the app."""
    database.initialize_database()
    
    if not database.get_setting("email"):
        prompt_credentials()
        totp_auth.initialize_totp()
    
    # Prompt for TOTP verification
    root = tk.Tk()
    root.withdraw()
    user_code = simpledialog.askstring("TOTP Authentication", "Enter your TOTP code:", show='*')
    if not totp_auth.verify_totp(user_code):
        messagebox.showerror("Authentication Failed", "Invalid TOTP Code. Exiting.")
        return
    
    print("Authentication successful!")
    gui.root.mainloop()

if __name__ == "__main__":
    main()
