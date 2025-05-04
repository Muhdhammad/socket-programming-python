import socket
import os

# port number
PORT = 12345

def send_file(s):
    # Connection to server
    try:
        s.connect((HOST, PORT))
        print("Connection successful")
    except:
        print("Unable to connect")
        exit(0)

    # Get file name from user
    file_name = input("Enter file name to send: ")

    # if file not exist throw error
    if not os.path.exists(file_name):
        raise ValueError("file not found")
    
    # get file size
    file_size = os.path.getsize(file_name)

    # Send file infp (file name and size) to server
    s.send(file_name.encode())
    s.send(str(file_size).encode())

    # Send file data
    with open(file_name, 'rb') as f:
        sent = 0
        while sent < file_size:
            data = f.read(4096)
            if not data: 
                break
            s.sendall(data) # send all data
            sent += len(data)

    print(f"Successfully sent {file_name} ({file_size} bytes)")

# host server name to estabilish connection
HOST = input("Enter server hostname: ")

# TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# function to send file
send_file(s)
s.close()