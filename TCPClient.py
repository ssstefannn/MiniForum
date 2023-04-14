import socket
import time

# session identification of the logged in user
session_id = -1

# flag to remember user state
chatting_with_user = False
chatting_with_all = False

def register_the_user(data, client_socket):
    client_socket.sendall(data.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(response)

def login_the_user(data, client_socket):
    client_socket.sendall(data.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    session_id = int(response)

def logout_the_user(data, client_socket):
    # add the session id
    data = f'{data} {session_id}'
    client_socket.sendall(data.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(response)
    session_id = -1

def chat_with_user(data, client_socket):
    data = f'{data} {session_id}'
    client_socket.sendall(data.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(response)
    chatting_with_user = True

def send_message(data, client_socket):
    if not chatting_with_user and not chatting_with_all:
        print('Invalid state')
        return
    data = f'{data} {session_id}'
    client_socket.sendall(data.encode('utf-8'))


while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 6666)
    client_socket.connect(server_address)
    data = input('Enter something\n')
    arguments = data.split()
    command = arguments[0]
    if command == '/register':
        register_the_user(data, client_socket)
    elif command == '/login':
        login_the_user(data, client_socket)
    elif command == '/logout':
        logout_the_user(data, client_socket)
    elif command == '/chat':
        chat_with_user(data, client_socket)
    else:
        send_message(data, client_socket)
client_socket.close()
    
