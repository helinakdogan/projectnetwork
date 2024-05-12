import socket
import json
import time

serverAddress = ('', 6000)
clients = {}

def saveUsers(data):
    file_path = 'users.json'
    with open(file_path, 'w') as file:
        json.dump(data, file)

def printOnlineUsers(usernames):
    for username in usernames:
        print(f"{username} is online!")

print("UDP Server is listening...")
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
serverSocket.bind(serverAddress)
while True:
    data, clientAddress = serverSocket.recvfrom(1024)
    jsonData = json.loads(data.decode())
    username = jsonData.get('username')
    clients[username] = (clientAddress[0] , time.time())
    saveUsers(clients)
    printOnlineUsers([username])
    time.sleep(8)
