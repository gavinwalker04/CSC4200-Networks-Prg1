# Design Explanation Document

## Overview
This document provides:
 - Description of how the client and server communicate.
 - Explanation of threading model chosen
 - Overview of how encryption is implemented

---

## **1. Client-Server Communication Model**
### **How the Client and Server Communicate**
The client and server communicate using the **TCP (Transmission Control Protocol)** model. The **process** is as follows:

1. **Server Start-Up**  
   - The server starts and listens for incoming client connections.
   - It binds to a **specific IP address (`HOST`) and port (`PORT`)**.
   - For HOST we are using our localhost IP address
   - For PORT here we are using PORT 5050
   - It continuously **accepts multiple client connections**.

2. **Client Connection**  
   - The client connects to the server via **TCP sockets**.
   - It establishes a **persistent connection** for message exchange.
   - It prompts the user to send a message.

3. **Message Transmission**  
   - The client **encrypts the entered message** using **AES-CBC** from Pycryptodome.
   - The **encrypted message** is sent to the server.

4. **Server Message Handling**  
   - The server receives the **encrypted message**.
   - If valid, it **decrypts the message** and logs it to the screen and the server_logs.txt file.

5. **Acknowledgment**  
   - The server encrypts a response (`"Message received"`) and sends it back to the client.
   - The client decrypts the acknowledgment and displays it.

6. **Client Disconnection**  
   - If the client sends `"!DISCONNECT"`, the server **closes the connection gracefully**.

---

## **2. Threading Model**
### **Multi-Threaded Server Design**
The server uses **Python's `threading` module** to handle **multiple clients simultaneously**. The threading model is implemented as follows:

- The **main server thread** continuously listens for incoming connections.
- When a new client connects:
  1. A **new thread is created** for that client.
  2. The **client’s messages are handled in its own thread**, allowing multiple clients to send messages at the same time.
  3. The main server remains free to accept new connections.

### **Benefits that this provides**

 **Concurrency** – Allows multiple clients to communicate with the server simultaneously.  
 **Non-Blocking** – The server does not get stuck waiting for one client.  
 **Better Performance** – Prevents slowdowns when handling multiple connections.  

---

## **3. Encryption and Security**
### **AES Encryption (CBC Mode)**
The client and server use **AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode** for message encryption.

1. **Key Management**
   - A **32-byte secret key** (`KEY`) is shared between the client and server.
   - A **random 16-byte IV (Initialization Vector)** is generated for each message to ensure security.

2. **Encryption Process**
   - The client **pads** the message to a multiple of 16 bytes.
   - It encrypts the message using **AES-CBC mode** and our encrypt function.
   - The **IV + Encrypted Message** is then sent to the server.

3. **Decryption Process**
   - The server extracts the **IV** from the received message.
   - It decrypts the message using the **same secret key** and our decrypt function.
   - It **removes padding** to retrieve the original message.
  
### Server -> Client
The process is basically the same for whenever a server sends to the client

1. **Encryption Process**
   - The server **pads** the message to a multiple of 16 bytes.
   - It encrypts the message using **AES-CBC mode** and our encrypt function.
   - The **IV + Encrypted Message** is then sent to the client.

2. **Decryption Process**
   - The client extracts the **IV** from the received message.
   - It decrypts the message using the **same secret key** and our decrypt function.
   - It **removes padding** to retrieve the original message.
---
