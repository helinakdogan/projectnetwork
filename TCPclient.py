import socket
import json
import time
import os
from cryptography.fernet import Fernet
import base64

with open('usernames.json', 'r') as file:
    user = json.load(file)
    username = user['username']

def showUserStatus():
    global data
    filePath = 'users.json'
    with open(filePath, 'r') as file:
        data = json.load(file)

    currentTime = time.time()
    usersStatus = "Status of users:\n"
    for username, clientInfo in data.items():
        lastActivity = clientInfo[1] 
        if currentTime - lastActivity < 10:
            status = "(Online)"
        elif currentTime - lastActivity >= 10:
            status = "(Away)"
        elif currentTime - lastActivity >= 900:
            del data[username]
        usersStatus += f"{username} {status}\n"
    print(usersStatus)

def chat():
    chatInitiator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_ID = input("Type name of the user you want to chat with:")
    addr = (data[client_ID][0], 6001)
    chatInitiator.connect(addr)
    secure = input("Type chat option (1 for encrypted, 2 for unencrypted): ")
    if secure == '1':
        secretKey = int(input("Choose your secret key: "))
        key = ((5^secretKey) % 23)
        jsonPayload = {"user": username, "key": key}
        chatInitiator.send(json.dumps(jsonPayload).encode())      
        tempkey = chatInitiator.recv(2048).decode()
        if tempkey:
            finalkey = (int(tempkey) ^ secretKey) % 23
            integer_bytes = int.to_bytes(finalkey, length=32, byteorder='big')
            fernet_key = base64.urlsafe_b64encode(integer_bytes)
            f = Fernet(fernet_key)
            message = input('Type your message: ')
            encrypted_message_bytes = f.encrypt(message.encode())
            encrypted_message_base64 = base64.b64encode(encrypted_message_bytes).decode()
            jsonPayload = {"user": username, "encrypted_message": encrypted_message_base64}
            chatInitiator.send(json.dumps(jsonPayload).encode())
            logChat(username, message, "SENT", client_ID)

    elif secure == '2':
        message = input("Type your message: ")
        key = 0
        unencrypted_message = message
        jsonPayload = {"user": username, "key": key, "unencrypted_message": unencrypted_message}
        chatInitiator.send(json.dumps(jsonPayload).encode())
        logChat(username, message, "SENT", client_ID)
    chatInitiator.close()

def logChat(username, message, sent_or_received, client):
    folder = 'chatLogs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'{client}.txt')
    with open(file_path, 'a') as file:
        file.write(f'{time.ctime()} | {username}: {message} ({sent_or_received})\n')

def showHistory(client):
    folder = 'chatLogs'
    if not os.path.exists(folder):
        print("There is no chat history yet.")
        return
    filePath = os.path.join(folder, f'{client}.txt')
    if not os.path.exists(filePath):
        print(f"no chat history with {client}")
        return
    with open(filePath,'r') as file:
        print(file.read())

def menu():
    print("1. Users")
    print("2. Chat")
    print("3. History")
    nav = input("Choose an option (use the numbers): ")
    if nav == '1':
        showUserStatus()
    elif nav == '2':
        chat()
    elif nav == '3':
        client = input("Type name of the user you want to see your chat history:")
        showHistory(client)
    else:
        print("Invalid input. Please try again.")
while True:
    menu()
