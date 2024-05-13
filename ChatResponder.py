import socket
import json 
import time
import os
from cryptography.fernet import Fernet
import base64

# Create a TCP socket for the chat responder
chatResponder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Define the server address and port
serverAddress = ('', 6001)  
# Bind the socket to the server address and port
chatResponder.bind(serverAddress)
# Listen for incoming connections
chatResponder.listen(1)  

# Display a message indicating that the TCP server is listening
print("TCP server is listening...")

# Function to log chat messages
def logChat(username, message, sent_or_received, encrypted=True):
    folder = 'chatLogs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'{username}.txt')
    with open(file_path, 'a') as file:
        # Log the message with timestamp, sender/receiver information, and encryption status
        encryption_status = " | Encrypted" if encrypted else " | Unencrypted"
        file.write(f'{time.ctime()} | {username}: {message} ({sent_or_received}{encryption_status})\n')

# Main loop to handle incoming connections
while True:
    # Accept incoming connection
    clientSocket, clientAddress = chatResponder.accept()
    returnIP = clientAddress[0]
    # Receive JSON payload from client
    jsonPayload = json.loads(clientSocket.recv(1024).decode())
    # Extract username from JSON payload
    username = jsonPayload['user']
    
    # Check if the message is encrypted or not
    if jsonPayload.get('key') == 0:
        # Message is not encrypted
        print(f"{username}: {jsonPayload.get('unencrypted_message')}")
        # Log the received message
        logChat(username, jsonPayload.get('unencrypted_message'), "RECEIVED", encrypted=False)
        # Close the connection
        clientSocket.close()
    else:
        # Message is encrypted
        # Prompt user to enter the secret key
        secretkey = int(input("enter your key: "))
        # Calculate the decryption key
        key = (5 ^ secretkey) % 23
        # Send the decryption key to the client
        clientSocket.send(str(key).encode())
        
        # Receive the final decryption key from the client
        finalkey = (int(jsonPayload['key']) ^ secretkey) % 23
        integer_bytes = int.to_bytes(finalkey, length=32, byteorder='big')
        fernet_key = base64.urlsafe_b64encode(integer_bytes)
        f = Fernet(fernet_key)
        
        # Receive encrypted message from the client
        receivedData = clientSocket.recv(2048)
        if receivedData:
            # Decrypt the message
            jsonPayload = json.loads(receivedData.decode())
            message = jsonPayload.get("encrypted_message")
            if message:
                decrypted_message = f.decrypt(base64.b64decode(message)).decode()
                # Print the decrypted message
                print(f"{username}: {decrypted_message}")
                # Log the received message
                logChat(username, decrypted_message, "RECEIVED", encrypted=True)
        # Close the connection
        clientSocket.close()
