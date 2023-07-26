import socket
import subprocess
import json
import sqlite3

def receive_message():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific IP and port
    host_ip = '127.0.0.1'  # Use '0.0.0.0' to listen on all available network interfaces
    port = 12345           # Use the same port number as in the sender script

    s.bind((host_ip, port))

    # Start listening for incoming connections
    s.listen()

    # Accept a connection from the sender
    conn, addr = s.accept()

    # Receive data from the sender
    data = conn.recv(1024).decode()

    # Close the connection and the socket
    conn.close()
    s.close()

    # Deserialize the received JSON string to a Python dictionary
    received_message = json.loads(data)

    return received_message

def send_message(message):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the receiver's IP address and port
    receiver_ip = '127.0.0.2'  # Replace with the receiver's IP if running on a different machine
    receiver_port = 12345      # Choose a free port number

    # Connect to the receiver
    s.connect((receiver_ip, receiver_port))

    # Serialize the message dictionary to a JSON string
    message_json = json.dumps(message)

    # Send the message
    s.sendall(message_json.encode())

    # Close the socket
    s.close()

def get_all_users():
    # Function to fetch all users from the database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

if __name__ == '__main__':
    from load_message import load_message
    print(load_message)

    while True:
        print("\n\nListening for messages...\n")
        # Receive a message from the sender
        # message format: {"message": "save_password", "password": "abc123"}
        # available commands: "save_password", "number_of_users"
        # to add: ""
        received_message = receive_message()
        print("Received message:", received_message)

        if received_message["message"] == "save_password":
            print("Saving password...")    
            # Run login_microservice.py using subprocess
            try:
                subprocess.run(['python', 'login_microservice.py', '--password', received_message["password"]])
                print("Password saved!")
            except Exception as e:
                print("Error while running login_microservice.py:", e)
        elif received_message["message"] == "number_of_users":
            print("Getting number of users...")
            # Fetch all users from the database
            users = get_all_users()
            print("All Users:")
            for user in users:
                print("Username: '{}', Password: '{}'".format(user[1], user[2]))
            return_data = {"message": "return_number_of_users", "number_of_users": len(users)}
            try:
                send_message(return_data)
                print("Number of users sent!")
            except Exception as e:
                print("Error while sending message:", e)


        received_message = None
