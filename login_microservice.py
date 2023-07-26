import tkinter as tk
from tkinter import ttk
import sys
import sqlite3

PASSWORD = ""

def register():
    # Function to handle the user registration process
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username is available (not already taken)
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Username already taken, show an error message
        error_label.config(text="Username already taken!")
    else:
        # Username is available, save the new user data to the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                       (username, password))
        conn.commit()
        conn.close()

        # root.destroy()

def clear_main_window():
    # Function to clear the content of the main window
    for widget in main_window.winfo_children():
        widget.destroy()


def show_account_data(username):
    main_window.protocol("WM_DELETE_WINDOW", root.destroy)  # Bind main_window's close button to root.destroy()


    # Function to display account data in the main window
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()

    # Clear previous content in the main window
    clear_main_window()

    # Listbox to display entries
    entries_listbox = tk.Listbox(main_window)
    entries_listbox.pack(fill=tk.BOTH, expand=True)  # Adjust with window size

    # Fetch and display all entries for the user
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, password FROM entries WHERE user_id = ?', (user_data[0],))
    entries = cursor.fetchall()
    conn.close()

    clear_main_window()

    # Frame to contain the table header
    header_frame = tk.Frame(main_window)
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
    rows_frame = tk.Frame(main_window)
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
        remove_entry_button = tk.Button(rows_frame, text="Remove Entry", command=lambda row=entries.index(entry): remove_entry(username, row))
        remove_entry_button.grid(row=entries.index(entry), column=3)


    # For simplicity, let's assume the 'user_data' is a tuple with (id, username, password, permissions)
    # You can display the data in a more user-friendly format
    account_data_label = tk.Label(main_window, text=f"Username: {user_data[1]}\n")
    account_data_label.pack()

    # Button to add a new entry
    add_entry_button = tk.Button(main_window, text="Add Entry", command=lambda: show_entry_dialog(username))
    add_entry_button.pack()

    add_generated_password_button = tk.Button(main_window, text="Add Generated Password", command=lambda: add_generated_password(username))
    add_generated_password_button.pack()

def remove_entry(username, row):
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
    show_account_data(username)


def clear_main_window():
    # Function to clear the content of the main window
    for widget in main_window.winfo_children():
        widget.destroy()

def show_entry_dialog(username):
    # Function to display a dialog for adding a new entry
    entry_dialog = tk.Toplevel(main_window)
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

    save_button = tk.Button(entry_dialog, text="Save Entry", command=lambda: save_entry(username, name_entry.get(), password_entry.get()))
    save_button.pack()

    cancel_button = tk.Button(entry_dialog, text="Cancel", command=entry_dialog.destroy)
    cancel_button.pack()

def add_generated_password(username):
    # display name input dialog for the generated password
    name_dialog = tk.Toplevel(main_window)
    name_dialog.title("Add New Entry")
    name_dialog.geometry("300x100")

    name_label = tk.Label(name_dialog, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(name_dialog)
    name_entry.pack()

    # get generated password from main application
    password = ""

    save_button = tk.Button(name_dialog, text="Save Entry", command=lambda: save_entry(username, name_entry.get(), PASSWORD))
    save_button.pack()

def save_entry(username, name, password):
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
    show_account_data(username)


def login():
    # Function to handle the login process
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password match a user in the database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        # Successful login, show the account data in the main window, close the login window
        main_window.deiconify()  # Show the main window
        root.withdraw()  # Hide the login window
        show_account_data(username)
    else:
        # Invalid login, show an error message
        error_label.config(text="Invalid username or password")

if __name__ == "__main__":
    # Check if the '--password' argument is provided and get its value
    if '--password' in sys.argv:
        password_index = sys.argv.index('--password') + 1
        if password_index < len(sys.argv):
            PASSWORD = sys.argv[password_index]

    # Start the Tkinter event loop
    root = tk.Tk()
    root.title("Login Window")
    root.geometry("300x200")

    # Create and position the login form widgets
    username_label = tk.Label(root, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    login_button = tk.Button(root, text="Login", command=login)
    login_button.pack()

    register_button = tk.Button(root, text="Register", command=register)
    register_button.pack()

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    main_window = tk.Toplevel(root)  # Create the main window as a Toplevel window
    main_window.title("Main Window")
    main_window.geometry("600x400")
    main_window.withdraw()  # Hide the main window initially

    root.mainloop()
