import socket
from Forum import *

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 6666))
    server_socket.listen(100)
    print('Server listening on port 6666...')
    forum = Forum()
    while True:
        client_socket, address = server_socket.accept()
        print(f'Connection from {address} established.')
        data = client_socket.recv(1024).decode('utf-8')
        print(f'Received data: {data}')
        if data[0] == '/':
            arguments = data.split()
            command = arguments[0]
            if command == '/register':
                #register the user;
                forum.register_the_user(arguments, client_socket)
            elif command == '/login':
                #log in the user
                forum.login_the_user(arguments, client_socket)
            elif command == '/logout':
                #log out the user
                forum.logout_the_user(arguments, client_socket)
            elif command == '/weather':
                # get the current weather
                x = 0
            elif command == '/news':
                # get the news feed
                x = 0
            elif command == '/checkout_chat':
                forum.checkout_chat(arguments, client_socket)
            elif command == '/post_message':
                forum.post_message(data, client_socket)
            else:
                print(f'Invalid request')
        client_socket.close()

main()
