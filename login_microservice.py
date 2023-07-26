import tkinter as tk
import sqlite3
import sys

class PasswordBookApp:
    def __init__(self, root, password=None):
        self.root = root
        self.root.title("Login Window")
        self.root.geometry("300x200")

        # Create and position the login form widgets
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack()

        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack()

        self.main_window = tk.Toplevel(self.root)  # Create the main window as a Toplevel window
        self.main_window.title("Main Window")
        self.main_window.geometry("600x400")
        self.main_window.withdraw()  # Hide the main window initially

        # Initialize the password variable
        self.PASSWORD = password

    def register(self):
        # Function to handle the user registration process
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username is available (not already taken)
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Username already taken, show an error message
            self.error_label.config(text="Username already taken!")
        else:
            # Username is available, save the new user data to the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                           (username, password))
            conn.commit()
            conn.close()

    def clear_main_window(self):
        # Function to clear the content of the main window
        for widget in self.main_window.winfo_children():
            widget.destroy()

    def show_account_data(self, username):
        self.main_window.protocol("WM_DELETE_WINDOW", self.root.destroy)  # Bind main_window's close button to root.destroy()

        # Function to display account data in the main window
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        # Clear previous content in the main window
        self.clear_main_window()

        # Listbox to display entries
        self.entries_listbox = tk.Listbox(self.main_window)
        self.entries_listbox.pack(fill=tk.BOTH, expand=True)  # Adjust with window size

        # Fetch and display all entries for the user
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, password FROM entries WHERE user_id = ?', (user_data[0],))
        entries = cursor.fetchall()
        conn.close()

        self.clear_main_window()

        # Frame to contain the table header
        header_frame = tk.Frame(self.main_window)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Create labels for each column header
        id_label = tk.Label(header_frame, text="ID", width=10, anchor=tk.W)
        id_label.grid(row=0, column=0)

        name_label = tk.Label(header_frame, text="Name", width=30, anchor=tk.W)
        name_label.grid(row=0, column=1)

        password_label = tk.Label(header_frame, text="Password", width=30, anchor=tk.W)
        password_label.grid(row=0, column=2)

        # Fetch and display all entries for the user
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, password FROM entries WHERE user_id = ?', (user_data[0],))
        entries = cursor.fetchall()
        conn.close()

        # Frame to contain the table rows
        rows_frame = tk.Frame(self.main_window)
        rows_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for index, entry in enumerate(entries):
            # Create labels for each column in the row
            id_entry = tk.Label(rows_frame, text=entry[0], width=10, anchor=tk.W)
            id_entry.grid(row=index, column=0)

            name_entry = tk.Label(rows_frame, text=entry[1], width=30, anchor=tk.W)
            name_entry.grid(row=index, column=1)

            password_entry = tk.Label(rows_frame, text=entry[2], width=30, anchor=tk.W)
            password_entry.grid(row=index, column=2)

            # Create a "Remove Entry" button for each row
            remove_entry_button = tk.Button(rows_frame, text="Remove Entry", command=lambda row=entries.index(entry): self.remove_entry(username, row))
            remove_entry_button.grid(row=entries.index(entry), column=3)

        # reformat, user_data = (id, username, password)
        account_data_label = tk.Label(self.main_window, text=f"Username: {user_data[1]}\n")
        account_data_label.pack()

        # Button to add a new entry
        add_entry_button = tk.Button(self.main_window, text="Add Entry", command=lambda: self.show_entry_dialog(username))
        add_entry_button.pack()

        add_generated_password_button = tk.Button(self.main_window, text="Add Generated Password", command=lambda: self.add_generated_password(username))
        add_generated_password_button.pack()

    def remove_entry(self, username, row):
        # Function to remove an entry from the database
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM entries WHERE user_id = ?', (user_id,))
        entry_id = cursor.fetchall()[row][0]
        cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
        conn.commit()
        conn.close()

        # Refresh the account data window to show the updated list
        self.show_account_data(username)

    def show_entry_dialog(self, username):
        # Function to display a dialog for adding a new entry
        entry_dialog = tk.Toplevel(self.main_window)
        entry_dialog.title("Add New Entry")
        entry_dialog.geometry("300x200")

        name_label = tk.Label(entry_dialog, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(entry_dialog)
        name_entry.pack()

        password_label = tk.Label(entry_dialog, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(entry_dialog, show="*")
        password_entry.pack()

        save_button = tk.Button(entry_dialog, text="Save Entry", command=lambda: self.save_entry(username, name_entry.get(), password_entry.get()))
        save_button.pack()

        cancel_button = tk.Button(entry_dialog, text="Cancel", command=entry_dialog.destroy)
        cancel_button.pack()

    def add_generated_password(self, username):
        # display name input dialog for the generated password
        name_dialog = tk.Toplevel(self.main_window)
        name_dialog.title("Add New Entry")
        name_dialog.geometry("300x100")

        name_label = tk.Label(name_dialog, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(name_dialog)
        name_entry.pack()

        # get generated password from main application
        password = self.PASSWORD

        save_button = tk.Button(name_dialog, text="Save Entry", command=lambda: self.save_entry(username, name_entry.get(), password))
        save_button.pack()

    def save_entry(self, username, name, password):
        # Function to save the new entry to the database
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO entries (user_id, name, password) VALUES (?, ?, ?)',
                       (user_id, name, password))
        conn.commit()
        conn.close()

        # Refresh the account data window to show the updated list
        self.show_account_data(username)

    def login(self):
        # Function to handle the login process
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username and password match a user in the database
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Successful login, show the account data in the main window, close the login window
            self.main_window.deiconify()  # Show the main window
            self.root.withdraw()  # Hide the login window
            self.show_account_data(username)
        else:
            # Invalid login, show an error message
            self.error_label.config(text="Invalid username or password")

if __name__ == "__main__":
    password_arg = None
    if '--password' in sys.argv:
        password_index = sys.argv.index('--password') + 1
        if password_index < len(sys.argv):
            password_arg = sys.argv[password_index]

    root = tk.Tk()
    app = PasswordBookApp(root, password=password_arg)
    root.mainloop()

