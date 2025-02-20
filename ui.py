import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3

class EmailManagerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Organizational Email Manager")
        self.root.geometry("800x600")
        
        # Create UI Components
        self.create_menu()
        self.create_main_panel()
    
    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)
    
    def create_main_panel(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.member_listbox = tk.Listbox(frame)
        self.member_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.member_listbox.bind("<Double-Button-1>", self.open_email_dialog)
        
        self.load_members()
    
    def load_members(self):
        conn = sqlite3.connect("email_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM members")
        members = cursor.fetchall()
        conn.close()
        
        for member in members:
            self.member_listbox.insert(tk.END, member[0])
    
    def open_email_dialog(self, event):
        selected_member = self.member_listbox.get(tk.ACTIVE)
        if not selected_member:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Send Email to {selected_member}")
        dialog.geometry("400x300")
        
        tk.Label(dialog, text="Description:").pack()
        description_entry = tk.Text(dialog, height=5)
        description_entry.pack(fill=tk.BOTH, expand=True)
        
        attach_button = tk.Button(dialog, text="Attach File", command=lambda: filedialog.askopenfilename())
        attach_button.pack()
        
        send_button = tk.Button(dialog, text="Send", command=lambda: self.send_email(selected_member, description_entry.get("1.0", tk.END)))
        send_button.pack()
    
    def send_email(self, recipient, description):
        messagebox.showinfo("Email Sent", f"Email sent to {recipient} successfully!")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EmailManagerUI()
    app.run()
