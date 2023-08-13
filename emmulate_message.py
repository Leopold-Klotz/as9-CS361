import socket
import json
import asyncio

async def receive_message():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific IP and port
    host_ip = '127.0.0.1'
    port = 12346

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

    print("Received message: " + str(received_message))

    return received_message

async def send_message(message):
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
    message2 = {"message": "number_of_users"}
    message3 = {"message": "check_users"}

    task_1 = send_message(message3)
    task_2 = receive_message()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(task_1, task_2))
    loop.close()

    print(task_2)