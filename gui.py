import tkinter as tk
from tkinter import messagebox, filedialog
import database
import email_handler

def open_email_dialog():
    """Opens a dialog for composing and sending an email."""
    dialog = tk.Toplevel(root)
    dialog.title("Compose Email")
    dialog.geometry("400x300")
    
    tk.Label(dialog, text="Recipient:").pack()
    recipient_entry = tk.Entry(dialog, width=50)
    recipient_entry.pack()
    
    tk.Label(dialog, text="Subject:").pack()
    subject_entry = tk.Entry(dialog, width=50)
    subject_entry.pack()
    
    tk.Label(dialog, text="Message:").pack()
    message_text = tk.Text(dialog, height=5)
    message_text.pack()
    
    def send_email():
        recipient = recipient_entry.get()
        subject = subject_entry.get()
        message = message_text.get("1.0", tk.END)
        success = email_handler.send_email(recipient, subject, message)
        if success:
            messagebox.showinfo("Success", "Email sent successfully!")
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to send email.")
    
    send_button = tk.Button(dialog, text="Send", command=send_email)
    send_button.pack()

def load_members():
    """Loads members into the listbox."""
    member_listbox.delete(0, tk.END)
    members = database.get_members()
    for member in members:
        member_listbox.insert(tk.END, f"{member[0]} - {member[1]} ({member[2]})")

def add_member():
    """Opens a dialog for adding a new member."""
    dialog = tk.Toplevel(root)
    dialog.title("Add Member")
    dialog.geometry("300x200")
    
    tk.Label(dialog, text="Name:").pack()
    name_entry = tk.Entry(dialog, width=40)
    name_entry.pack()
    
    tk.Label(dialog, text="Email:").pack()
    email_entry = tk.Entry(dialog, width=40)
    email_entry.pack()
    
    tk.Label(dialog, text="Position:").pack()
    position_entry = tk.Entry(dialog, width=40)
    position_entry.pack()
    
    def save_member():
        name, email, position = name_entry.get(), email_entry.get(), position_entry.get()
        if name and email and position:
            database.add_member(name, email, position)
            load_members()
            dialog.destroy()
        else:
            messagebox.showerror("Error", "All fields are required.")
    
    save_button = tk.Button(dialog, text="Add", command=save_member)
    save_button.pack()

# Main GUI window
root = tk.Tk()
root.title("Email Manager Dashboard")
root.geometry("800x500")

tk.Button(root, text="Compose Email", command=open_email_dialog).pack()
tk.Button(root, text="Add Member", command=add_member).pack()

member_listbox = tk.Listbox(root)
member_listbox.pack(fill=tk.BOTH, expand=True)

load_members()
root.mainloop()