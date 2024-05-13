import socket
import json
import time
import os
from cryptography.fernet import Fernet
import base64

# Load the username from the usernames.json file
with open('usernames.json', 'r') as file:
    user = json.load(file)
    username = user['username']

# Function to display the status of users (online, away)
def showUserStatus():
    global data
    # Load user data from the users.json file
    filePath = 'users.json'
    with open(filePath, 'r') as file:
        data = json.load(file)

    currentTime = time.time()
    usersStatus = "Status of users:\n"
    # Check each user's last activity time to determine their status
    for username, clientInfo in data.items():
        lastActivity = clientInfo[1] 
        if currentTime - lastActivity < 10:
            status = "(Online)"
        elif currentTime - lastActivity >= 10:
            status = "(Away)"
        elif currentTime - lastActivity >= 900:
            # Remove user data if inactive for more than 15 minutes (900 seconds)
            del data[username]
        usersStatus += f"{username} {status}\n"
    print(usersStatus)

# Function to initiate a chat with another user
def chat():
    chatInitiator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_ID = input("Type name of the user you want to chat with:")
    addr = (data[client_ID][0], 6001)
    chatInitiator.connect(addr)
    secure = input("Type chat option (1 for encrypted, 2 for unencrypted): ")
    if secure == '1':
        # If encrypted chat is selected
        secretKey = int(input("Choose your secret key: "))
        key = ((5^secretKey) % 23)
        # Send the encryption key to the recipient
        jsonPayload = {"user": username, "key": key}
        chatInitiator.send(json.dumps(jsonPayload).encode())      
        tempkey = chatInitiator.recv(2048).decode()
        if tempkey:
            # Calculate the final decryption key
            finalkey = (int(tempkey) ^ secretKey) % 23
            integer_bytes = int.to_bytes(finalkey, length=32, byteorder='big')
            fernet_key = base64.urlsafe_b64encode(integer_bytes)
            f = Fernet(fernet_key)
            message = input('Type your message: ')
            # Encrypt the message and send it
            encrypted_message_bytes = f.encrypt(message.encode())
            encrypted_message_base64 = base64.b64encode(encrypted_message_bytes).decode()
            jsonPayload = {"user": username, "encrypted_message": encrypted_message_base64}
            chatInitiator.send(json.dumps(jsonPayload).encode())
            # Log the sent message
            logChat(username, message, "SENT | Encrypted", client_ID)

    elif secure == '2':
        # If unencrypted chat is selected
        message = input("Type your message: ")
        key = 0
        unencrypted_message = message
        # Send the message without encryption
        jsonPayload = {"user": username, "key": key, "unencrypted_message": unencrypted_message}
        chatInitiator.send(json.dumps(jsonPayload).encode())
        # Log the sent message
        logChat(username, message, "SENT | Unencrypted", client_ID)
    chatInitiator.close()

# Function to log chat messages
def logChat(username, message, sent_or_received, client):
    folder = 'chatLogs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'{client}.txt')
    with open(file_path, 'a') as file:
        # Log the message with timestamp, sender/receiver information, and encryption status
        file.write(f'{time.ctime()} | {username}: {message} ({sent_or_received})\n')

# Function to display chat history with a specific user
def showHistory(client):
    folder = 'chatLogs'
    if not os.path.exists(folder):
        print("There is no chat history yet.")
        return
    filePath = os.path.join(folder, f'{client}.txt')
    if not os.path.exists(filePath):
        print(f"No chat history with {client}")
        return
    with open(filePath,'r') as file:
        # Display chat history with the specified user
        print(file.read())

# Function to display menu options and handle user input
def menu():
    print("1. Users")
    print("2. Chat")
    print("3. History")
    nav = input("Choose an option (use the numbers): ")
    if nav == '1':
        # Option to display user status
        showUserStatus()
    elif nav == '2':
        # Option to initiate a chat
        chat()
    elif nav == '3':
        # Option to view chat history
        client = input("Type name of the user you want to see your chat history:")
        showHistory(client)
    else:
        print("Invalid input. Please try again.")

# Main loop to display the menu continuously
while True:
    menu()
