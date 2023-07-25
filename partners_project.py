import tkinter as tk
from tkinter import ttk
import datetime
import random
import re
import string

name_storage = []
date_storage = []
number_storage = []

name_storage_for_display = []
date_storage_for_display = []

special_chars = ["!", "@", "#", "$", "%", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", "|", ";", ":",
                 "<", ">", ",", ".", "?"]


def reset_data():
    # Clear the stored items
    name_storage.clear()
    date_storage.clear()
    number_storage.clear()
    name_storage_for_display.clear()
    date_storage_for_display.clear()

    # Update the display
    update_display()


def update_display():
    label_for_names.config(text="Names: " + ", ".join(name_storage_for_display))
    label_for_numbers.config(text="Numbers: " + ", ".join(number_storage))
    label_for_dates.config(text="Dates: " + ", ".join(date_storage_for_display))


def data_submit():
    # Get input from the input text area and split it up by line
    list_of_names = name_input_area.get('1.0', tk.END).splitlines()
    for name in list_of_names:
        if name:
            if name not in name_storage_for_display:
                # Add full names for display
                name_storage_for_display.append(name)
                # Break up names into single names for password calculation
                name_separated = name.split()
                name_storage.extend(name_separated)

    list_of_numbers = number_input_area.get('1.0', tk.END).splitlines()
    for number in list_of_numbers:
        if number:
            if number not in number_storage:
                number_storage.append(number)

    list_of_dates = date_input_area.get('1.0', tk.END).splitlines()
    for date in list_of_dates:
        if date:  # Add this line to ignore empty strings
            if date not in date_storage_for_display:
                date_storage_for_display.append(date)
                date_object = datetime.datetime.strptime(date, "%Y-%m-%d")
                separated_year = date_object.strftime("%Y")
                separated_month = date_object.strftime("%m")
                separated_day = date_object.strftime("%d")
                date_storage.extend([separated_year, separated_month, separated_day])

    update_display()


def password_generation():
    # Select Random Name
    random_name_index = random.randint(0, len(name_storage) - 1)
    name = name_storage[random_name_index]

    # Select Random Name
    random_number_index = random.randint(0, len(number_storage) - 1)
    number = number_storage[random_number_index]

    # Select Random Name
    random_date_index = random.randint(0, len(date_storage) - 1)
    date = date_storage[random_date_index]

    password_list = [name, number, date]

    shuffled_list = random.sample(password_list, len(password_list))

    password_list = []

    password = "".join(shuffled_list)

    special_char_present = False
    for char in special_chars:
        if char in password:
            special_char_present = True
            break
    # Add a random special character if none is present
    if not special_char_present:
        random_special_char = random.choice(special_chars)
        password += random_special_char

    special_char_present = False

    label_for_password.config(text="Password: " + password)


def check_password_strength(password):
    # The password score starts at 0
    score = 0

    if len(password):
        # Increase the score if the password has a good length
        if len(password) > 8:
            score += 2

        # Increase the score if the password contains both lower and uppercase letters
        if re.search("[a-z]", password) and re.search("[A-Z]", password):
            score += 2

        # Increase the score if the password contains at least one number
        if re.search("\d", password):
            score += 2

        # Increase the score if the password contains at least one special character
        if any(char in special_chars for char in password):
            score += 2

        weak_patterns = ['123', 'abc', 'qwerty', 'password', 'admin', 'login', 'aaa','chocolate', 'cookie', 'monkey',
                         'sunshine', 'welcome', 'football', 'baseball', 'dragon', 'letmein', 'iloveyou',
                         'master', 'superman', 'shadow', 'batman']

        # Convert the password to lowercase
        lower_password = password.lower()

        # Check if the password contains any of the weak patterns
        if any(pattern in lower_password for pattern in weak_patterns):
            score -= 2

    # Make sure the score is not negative or above 10
    score = max(0, min(score, 10))

    return score


def check_password():
    password = pass_check_input_area.get("1.0", tk.END).strip()
    score = check_password_strength(password)
    password_score_label.config(text="Password strength: " + str(score))


# Makes the display
root = tk.Tk()
root.configure(bg='light blue')

# Name input label
label1 = tk.Label(root, text="Please enter names you want considered for a password and separate by new line:",
                  bg = 'light blue')
label1.pack()
# Name Input area
name_input_area = tk.Text(root, height=5, width=50, bg='light blue')
name_input_area.pack()

# Number input label
label2 = tk.Label(root, text="Please enter numbers you want considered for a password and separate by new line:",
                  bg = 'light blue')
label2.pack()
# Number Area
number_input_area = tk.Text(root, height=5, width=50, bg='light blue')
number_input_area.pack()

# Date input label
label3 = tk.Label(root, text="Please enter the dates you want considered for a password in the format 'YYYY-MM-DD' "
                             "and separate by new line:", bg = 'light blue')
label3.pack()
# Number input Area
date_input_area = tk.Text(root, height=5, width=50, bg='light blue')
date_input_area.pack()

# submit button
submit_button = tk.Button(root, text="Submit Components for Password", command=data_submit, bg='light blue')
submit_button.pack()

# Create the display frame
display_frame = tk.Frame(root, bg='light blue')
display_frame.pack()

# Labels for fields inside of display frame
label_for_names = tk.Label(display_frame, text="", bg='light blue')
label_for_numbers = tk.Label(display_frame, text="", bg='light blue')
label_for_dates = tk.Label(display_frame, text="", bg='light blue')

label_for_names.pack()
label_for_numbers.pack()
label_for_dates.pack()

# Reset Button
reset_button = tk.Button(root, text="Reset", command=reset_data, bg='light blue')
reset_button.pack()

# Generate Password Button
password_button = tk.Button(root, text="Generate Password", command=password_generation, bg='light blue')
password_button.pack()

# Create the password label
label_for_password = tk.Label(root, text="", bg='light blue')
label_for_password.pack()

label_for_pass_check = tk.Label(root, text="Please enter the password whose security rating you would like checked")
label_for_pass_check.pack()

# Create the display frame
pass_check_frame = tk.Frame(root, bg='light blue')
pass_check_frame.pack()

pass_check_input_area = tk.Text(root, height=2, width=30, bg='light blue')
pass_check_input_area.pack()

password_score_label = tk.Label(pass_check_frame, text="", bg='light blue')
password_score_label.pack()

# Generate Score Button
score_button = tk.Button(root, text="Check Password Strength", command=check_password, bg='light blue')
score_button.pack()



root.mainloop()
