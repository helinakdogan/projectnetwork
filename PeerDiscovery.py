import socket
import json
import time

# Server address and port
serverAddress = ('', 6000)

# Dictionary to store clients' information
clients = {}

# Function to save users' data to a JSON file
def saveUsers(data):
    file_path = 'users.json'
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Function to print online users
def printOnlineUsers(usernames):
    for username in usernames:
        print(f"{username} is online!")

# Display a message indicating that the UDP server is listening
print("UDP Server is listening...")

# Create a UDP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Enable broadcast option
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Bind the socket to the server address and port
serverSocket.bind(serverAddress)

# Main loop to receive data from clients
while True:
    # Receive data and client address
    data, clientAddress = serverSocket.recvfrom(1024)
    # Decode received JSON data
    jsonData = json.loads(data.decode())
    # Extract username from the received data
    username = jsonData.get('username')
    # Store client information in the dictionary with the username as key
    clients[username] = (clientAddress[0], time.time())
    # Save updated user information to JSON file
    saveUsers(clients)
    # Print the online status of the user
    printOnlineUsers([username])
    # Wait for 8 seconds before processing the next message
    time.sleep(8)
