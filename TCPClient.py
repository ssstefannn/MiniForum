import socket
import time

session_id = -1

while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 6666)
    client_socket.connect(server_address)
    data = input('Enter something\n')
    client_socket.sendall(data.encode('utf-8'))
    print(f'Sent data: {data}')
    response = client_socket.recv(1024).decode('utf-8')
    print(f'Received response: {response}')
    if data == '/login':
        session_id = int(response)
client_socket.close()
    
