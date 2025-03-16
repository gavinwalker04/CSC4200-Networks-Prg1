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
DISCONNECT_MESSAGE = "!DISCONNECT"
KEY = b'This is a key123This is a key123'  # 32-byte AES key

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# AES Encryption Function
def encrypt(plaintext, key):
    """Encrypts a message using AES in CBC mode."""
    iv = os.urandom(16)  # Generate a random 16-byte IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return iv + ciphertext  # Prepend IV to ciphertext for decryption

# AES Decryption Function
def decrypt(ciphertext, key):
    """Decrypts a message using AES in CBC mode."""
    iv = ciphertext[:16]  # Extract IV from the message
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return plaintext.decode()

# handles the connection between the client and the server
def handle_clients(conn, addr):
    print(f"New Connection: {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  # Get message length
        if msg_length:
            msg_length = int(msg_length)
            encrypted_msg = conn.recv(msg_length)  # Receive encrypted message
            
            try:
                decrypted_msg = decrypt(encrypted_msg, KEY)  # Decrypt message
                print(f"{addr} : {decrypted_msg}")  # Print decrypted message
            except Exception as e:
                print(f"[ERROR] Failed to decrypt message from {addr}: {e}")
                continue

            # Handle disconnect message
            if decrypted_msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"{addr} : {decrypted_msg}")

            # Send encrypted acknowledgment
            ack_message = "Message received"
            encrypted_ack = encrypt(ack_message, KEY)
            conn.send(encrypted_ack)  # Send encrypted acknowledgment

    conn.close()

# handles new connections and sends where they need to go
def start():
    server.listen()
    print(f"Listening on {HOST}")
    while True:
        # when new connection occurs, stores address 
        # and object that allows us to send info back to that connection
        conn, addr = server.accept()

        # When new connection occcurs, pass to handle_clients
        # and starts the thread
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()

        # shows number of active client connections
        print(f"Active Connections:  {threading.active_count() - 1}")


print("Server is starting!")
start()