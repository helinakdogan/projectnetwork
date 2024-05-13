import socket
import json
import time

# Create a UDP socket for the client
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Enable broadcast option
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Define the server's UDP address and port
serverUDPaddress = ('192.168.0.106', 6000)

# Prompt the user to enter their username
clientUsername = input("Please, type your username:")
# Create a dictionary with the username
username = {'username': clientUsername}
# Define the file path to store the username
file_path = 'usernames.json'

# Write the username to a JSON file
with open(file_path, 'w') as file:
    json.dump(username, file)

# Convert the username dictionary to JSON format
username = json.dumps({'username': clientUsername})

# Display a message indicating that the user is connected to the UDP server
print(f"User {clientUsername} is connected to UDP Server")

# Main loop to send the username to the server every 8 seconds
while True:
    # Send the username to the server
    clientSocket.sendto(username.encode(), serverUDPaddress)
    # Wait for 8 seconds before sending the username again
    time.sleep(8)
