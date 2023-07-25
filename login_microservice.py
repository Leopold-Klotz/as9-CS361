import tkinter as tk
import sqlite3

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
        permissions = "some_permissions"  # You can set default permissions for new users
        cursor.execute('INSERT INTO users (username, password, permissions) VALUES (?, ?, ?)',
                       (username, password, permissions))
        conn.commit()
        conn.close()

        # Optionally, you can close the login window after successful registration
        root.destroy()


def show_account_data(username):
    # Function to display account data in the main window
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()

    # Clear previous content in the main window
    clear_main_window()

    # For simplicity, let's assume the 'user_data' is a tuple with (id, username, password, permissions)
    # You can display the data in a more user-friendly format
    account_data_label = tk.Label(main_window, text=f"Username: {user_data[1]}\nPermissions: {user_data[3]}")
    account_data_label.pack()

    # Button to add a new entry
    add_entry_button = tk.Button(main_window, text="Add Entry", command=lambda: show_entry_dialog(username))
    add_entry_button.pack()

    # Listbox to display entries
    entries_listbox = tk.Listbox(main_window)
    entries_listbox.pack()

    # Fetch and display all entries for the user
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, password FROM entries WHERE user_id = ?', (user_data[0],))
    entries = cursor.fetchall()
    conn.close()

    for entry in entries:
        entries_listbox.insert(tk.END, f"Name: {entry[0]}, Password: {entry[1]}")

def clear_main_window():
    # Function to clear the content of the main window
    for widget in main_window.winfo_children():
        widget.destroy()

def show_entry_dialog(username):
    # Function to display a dialog for adding a new entry
    entry_dialog = tk.Toplevel(main_window)
    entry_dialog.title("Add New Entry")

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
        # Successful login, show the account data in the main window
        main_window.deiconify()  # Show the main window
        show_account_data(username)
    else:
        # Invalid login, show an error message
        error_label.config(text="Invalid username or password")

if __name__ == "__main__":
    # Start the Tkinter event loop
    root = tk.Tk()
    root.title("Login Window")

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
    main_window.withdraw()  # Hide the main window initially

    root.mainloop()