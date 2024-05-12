import socket
import json 
import time
import os
from cryptography.fernet import Fernet
import base64

chatResponder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ('', 6001)  
chatResponder.bind(serverAddress)
chatResponder.listen(1)  

print("TCP server is listening...")

def logChat(username, message, sent_or_received):
    folder = 'chatLogs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'{username}.txt')
    with open(file_path, 'a') as file:
        file.write(f'{time.ctime()} | {username}: {message} ({sent_or_received})\n')

while True:
    clientSocket, clientAddress = chatResponder.accept()
    returnIP = clientAddress[0]
    jsonPayload = json.loads(clientSocket.recv(1024).decode())
    username = jsonPayload['user']
    if jsonPayload.get('key') == 0:
        print(f"{username}: {jsonPayload.get('unencrypted_message')}")
        logChat(username, jsonPayload.get('unencrypted_message'), "RECEIVED")
        clientSocket.close()
    else:
        secretkey = int(input("enter your key: "))
        key = (5 ^ secretkey) % 23
        clientSocket.send(str(key).encode())
        finalkey = (int(jsonPayload['key']) ^ secretkey) % 23
        integer_bytes = int.to_bytes(finalkey, length=32, byteorder='big')
        fernet_key = base64.urlsafe_b64encode(integer_bytes)
        f = Fernet(fernet_key)
        receivedData = clientSocket.recv(2048)
        if receivedData:
            jsonPayload = json.loads(receivedData.decode())
            message = jsonPayload.get("encrypted_message")
            if message:
                decrypted_message = f.decrypt(base64.b64decode(message)).decode()
                print(f"{username}: {decrypted_message}")
                logChat(username, decrypted_message, "RECEIVED")
        clientSocket.close()
