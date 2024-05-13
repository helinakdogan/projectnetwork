# Project Name: Online Chat Application
This project is an online chat application that utilizes UDP to discover users' online statuses and TCP to chat with users. Additionally, it includes a feature where users can review their chat histories and see the last time they were active.

# How It Works:
## User Registration and Server Connection:
Users initially enter a username.
This username is saved in a JSON file and sent to the server via UDP.
The server keeps track of this information to monitor the online statuses of other users.
## Online Status Discovery (UDP):
The server broadcasts updates at regular intervals (e.g., every 8 seconds) to inform clients about the online statuses of users.
## Chatting and Viewing Chat History (TCP):
Users can establish TCP connections to chat with other users.
Encrypted or unencrypted messages are sent and received via TCP.
Users can also connect to the server via TCP to view the chat history of a specific user.

# Limitations:
## Dependencies: The program requires pyDes, cryptography, and Python to be installed on the computer to function properly.
## Security: The encryption process is basic and may not provide sufficient security. Stronger encryption methods should be implemented.
## Authentication: Usernames and IP addresses are accepted without authentication. User identities should be authenticated and authorization should be implemented.
## Data Integrity: The integrity of incoming data is not verified. Measures should be taken to ensure the accuracy and integrity of data.
## Performance: The system may not efficiently handle large data traffic or numerous clients. Broadcasting updates at specific intervals may increase server load.
