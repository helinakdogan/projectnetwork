import socket
import json
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
serverUDPaddress = ('192.168.0.106', 6000)

clientUsername = input("Please, type your username:")
username = {'username': clientUsername}
file_path = 'usernames.json'

with open(file_path, 'w') as file:
    json.dump(username,file)

username = json.dumps({'username': clientUsername})

print(f"User {clientUsername} is connected to UDP Server")

while True:
    clientSocket.sendto(username.encode(), serverUDPaddress)
    time.sleep(8)  