import socket
import threading
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import os

# Configuration
HEADER = 64
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
ADDR = (HOST, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
KEY = b'This is a key123This is a key123'  # 32-byte AES key (Must be 16, 24, or 32 bytes)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

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

# Function to send encrypted messages to the server
def send_message(client, message):
    encrypted_message = encrypt(message, KEY)  # Encrypt message
    msg_length = str(len(encrypted_message)).encode(FORMAT)
    msg_length += b' ' * (HEADER - len(msg_length))  # Pad message length
    client.send(msg_length)
    client.send(encrypted_message)  # Send encrypted data

# Function to receive encrypted responses from the server
def receive_message(client):
    try:
        encrypted_response = client.recv(1024)  # Receive encrypted acknowledgment
        decrypted_response = decrypt(encrypted_response, KEY)  # Decrypt response
        print(f"[*] Server Response: {decrypted_response}")
    except Exception as e:
        print(f"[ERROR] Failed to decrypt server response: {e}")


# Start the client
def start():
    print("Connected to the server!")

    while True:
        message = input("Enter a message: ")

        if message:
            send_message(client, message)
            receive_message(client)  # Receive server acknowledgment

            if message == DISCONNECT_MESSAGE:
                break  # Exit loop if disconnect message is sent

    client.close()
    print("Disconnected from the server.")

start()