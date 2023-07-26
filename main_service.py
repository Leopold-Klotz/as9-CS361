import socket
import subprocess

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

    return data

if __name__ == '__main__':
    while True:
        # Receive a message from the sender
        # message format: {"message": "save_password", "password": "abc123"}
        # available commands: "save_password"
        received_message = receive_message()
        print("Received message:", received_message)

        if received_message["message"] == "save_password":
            print("Saving password...")
            
            # Run login_microservice.py using subprocess
            try:
                subprocess.run(['python', 'login_microservice.py', '--password', received_message["password"]])
            except Exception as e:
                print("Error while running login_microservice.py:", e)
        
        received_message = None
