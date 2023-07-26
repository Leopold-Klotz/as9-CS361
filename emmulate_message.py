import socket
import json

def send_message(message):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the receiver's IP address and port
    receiver_ip = '127.0.0.1'  # Replace with the receiver's IP if running on a different machine
    receiver_port = 12345      # Choose a free port number

    # Connect to the receiver
    s.connect((receiver_ip, receiver_port))

    # Serialize the message dictionary to a JSON string
    message_json = json.dumps(message)

    # Send the message
    s.sendall(message_json.encode())

    # Close the socket
    s.close()

if __name__ == '__main__':
    message = {"message": "save_password", "password": "abc123"}
    send_message(message)
