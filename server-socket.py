import socket
import os

PORT = 12345 # port number
MAX_FILE_SIZE = 10 * 1024 * 1024* 1024  # limit of 10 GB
DATA_DIR = "./received_data" # directory to store received files

def receive_file(conn):
    # Receive file name and file size
    file_name = conn.recv(1024).decode()
    file_size = int(conn.recv(1024).decode())

    if file_size > MAX_FILE_SIZE:
        raise ValueError("File size exceeds limit")

    # Create "received_data" directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_path = os.path.join(DATA_DIR, file_name)

    # Receive file data in chunks
    with open(file_path, "wb") as f:
        received = 0
        while received < file_size:
            data = conn.recv(4096) # receive upto 4096 bytes
            if not data: # handle unexpected connection loss
                raise ConnectionError("Connection lost during transfer")
            f.write(data)
            received += len(data)

    print(f"Successfully Received {file_name} ({received}/{file_size} bytes)")

# Server setup

# TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# get IP address dynamically 
HOST = socket.gethostbyname(socket.gethostname())
# bind and listen
s.bind((HOST, PORT))
s.listen()
print(f"Server listening on {HOST}:{PORT}")
# wait for client connnection
# conn -> new socket dedicated for this client
# addr -> clients (!P, PORT) tuple
conn, addr = s.accept()
# function to receive files
receive_file(conn)

s.close()
