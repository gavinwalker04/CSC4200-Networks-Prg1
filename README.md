# CSC4200-Networks-Prg1

# Simple Client-Server Program

This implements a **basic client-server model** using **TCP sockets** to facilitate communication between a server and multipe clients.

Uses **Python** with **AES encryption** for secure communication.

## Features
**Multi-threading** - Handles multiple client connections.  
**AES Encryption (CBC Mode)** - Ensures secure message transmission using Pycrptodome.  
**Message Logging** - The server logs received messages to the terminal and to `server_logs.txt`.  
**Graceful Error Handling** - Manages client disconnections properly as well as unexpected errors.  
**Acknowledgment** - Server sends responses back to clients and clients display that response.  

---

## **1. Required Libraries**
This project requires **Python 3** and the following dependencies:

### **Installing Python**

If Python is not already installed on your system, follow the steps below:

### **On Linux (Ubuntu/Debian)**

**Open a terminal and isntall python**
```bash
sudo apt update && sudo apt install python3
```
If this does not work refer to python documentation

**Verify Installation Success**
```bash
python3 --version
```

- `pycryptodome` (for AES encryption)
- `socket` (built-in for TCP communication)
- `threading` (built-in for handling multiple clients)

### **🔧 Installation Steps**
Run the following command to install the required library:
```bash
pip install pycryptodome
```
**Or**
```bash
pip3 install pycryptodome
```

## **2. How to Build and Run the Project**
The project uses a **Makefile** to automate running and cleaning up the code.

---

### **Running the Server**

**NO BUILD REQUIRED DUE TO USING PYTHON**

Start the server using the `Makefile`:
```bash
make run-server
```
Or manually
```bash
python3 server.py
```
Should display this:
```bash
Server is starting!
Listening on {ADDRESS}
```
---
### **Running the Client**
**In a different terminal**
```bash
make run-client
```
Or manually
```bash
python3 client.py
```
---
### **Disconnecting the Client**
```bash
!DISCONNECT
```
This will close the connection between the client and the server.

---
### **Cleaning**
To remove the logs file and the cached files
```bash
make clean
```

## **3. Explanation of Dependencies**
| **Dependency**  | **Purpose** |
|----------------|-------------|
| `socket`       | Handles TCP communication between client and server. |
| `threading`    | Allows the server to handle multiple clients concurrently. |
| `pycryptodome` | Provides AES encryption and decryption for secure message transmission. |
