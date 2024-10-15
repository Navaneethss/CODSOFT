import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class ContactBook(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Contact Book")
        self.geometry("600x400")

        self.connect_to_db()

        self.search_bar = tk.Entry(self, font=("Arial", 12))
        self.search_bar.pack(pady=10)
        self.search_bar.bind("<KeyRelease>", self.search_contacts)

        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Phone', 'Email', 'Address'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Address', text='Address')

        self.tree.pack(pady=20, fill='both', expand=True)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Contact", command=self.add_contact)
        self.update_button = tk.Button(self.button_frame, text="Update Contact", command=self.update_contact)
        self.delete_button = tk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact)

        self.add_button.grid(row=0, column=0, padx=10)
        self.update_button.grid(row=0, column=1, padx=10)
        self.delete_button.grid(row=0, column=2, padx=10)

        self.load_contacts()

    def connect_to_db(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            address TEXT)""")
        self.conn.commit()

    def load_contacts(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.cursor.execute("SELECT * FROM contacts ORDER BY id")
        rows = self.cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def add_contact(self):
        dialog = ContactDialog(self, "Add Contact")

        self.wait_window(dialog)
        if dialog.result:
            name, phone, email, address = dialog.result

            self.cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                                (name, phone, email, address))
            self.conn.commit()
            self.load_contacts()

    def update_contact(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Update Contact", "Please select a contact to update.")
            return

        selected_contact = self.tree.item(selected_item, 'values')

        dialog = ContactDialog(self, "Update Contact", contact=selected_contact)

        self.wait_window(dialog)
        if dialog.result:
            name, phone, email, address = dialog.result
            contact_id = selected_contact[0]

            self.cursor.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                                (name, phone, email, address, contact_id))
            self.conn.commit()
            self.load_contacts()

    def delete_contact(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Delete Contact", "Please select a contact to delete.")
            return

        selected_contact = self.tree.item(selected_item, 'values')
        contact_id = selected_contact[0]

        confirm = messagebox.askyesno("Delete Contact", f"Are you sure you want to delete contact ID {contact_id}?")
        if confirm:
            self.cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            self.conn.commit()
            self.load_contacts()

    def search_contacts(self, event=None):
        search_text = self.search_bar.get().strip()

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? ORDER BY id",
                            ('%' + search_text + '%', '%' + search_text + '%'))
        rows = self.cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

class ContactDialog(tk.Toplevel):
    def __init__(self, parent, title, contact=None):
        super().__init__(parent)

        self.title(title)
        self.result = None

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        if contact:
            self.name_var.set(contact[1])
            self.phone_var.set(contact[2])
            self.email_var.set(contact[3])
            self.address_var.set(contact[4])

        tk.Label(self, text="Name:").pack(pady=5)
        tk.Entry(self, textvariable=self.name_var).pack(pady=5)

        tk.Label(self, text="Phone:").pack(pady=5)
        tk.Entry(self, textvariable=self.phone_var).pack(pady=5)

        tk.Label(self, text="Email:").pack(pady=5)
        tk.Entry(self, textvariable=self.email_var).pack(pady=5)

        tk.Label(self, text="Address:").pack(pady=5)
        tk.Entry(self, textvariable=self.address_var).pack(pady=5)

        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

    def on_submit(self):
        self.result = (
            self.name_var.get(),
            self.phone_var.get(),
            self.email_var.get(),
            self.address_var.get()
        )
        self.destroy()


if __name__ == "__main__":
    app = ContactBook()
    app.mainloop()
