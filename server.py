import socket
import threading
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import os

# Configuration
HEADER = 64
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# handles the connection between the client and the server
def handle_clients(conn, addr):
    print(f"New Connection: {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Gets length of message
        msg_length = int(msg_length) # Makes length into a int
        msg = conn.recv(msg_length).decode(FORMAT) # Gets actual message
        print(f"{addr} : {msg}") # prints the message

# handles new connections and sends where they need to go
def start():
    server.listen()
    while True:
        # when new connection occurs, stores address 
        # and object that allows us to send info back to that connection
        conn, addr = server.accept()

        # When new connection occcurs, pass to handle_clients
        # and starts the thread
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()

        # shows number of active client connections
        print(f"Active Connections:  {threading.activeCount() - 1}")


print("Server is starting!")
start()