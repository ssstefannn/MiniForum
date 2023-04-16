import socket
from ClientApi import *

def main():
    api = ClientApi()
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 4321)
        client_socket.connect(server_address)
        data = input(f'Enter a command: /register, /login, /logout, /checkout_chat, /post_message, /get_news, /get_weather\n')
        arguments = data.split()
        command = arguments[0]
        if command == '/register':
            api.register_the_user(data, client_socket)
        elif command == '/login':
            api.login_the_user(data, client_socket)
        elif command == '/logout':
            api.logout_the_user(data, client_socket)
        elif command == '/checkout_chat':
            api.checkout_chat(data, client_socket)
        elif command == '/post_message':
            api.post_message(data, client_socket)
        elif command == '/get_news':
            api.get_news(data, client_socket)
        elif command == '/get_weather':
            api.get_weather(data, client_socket)
        else:
            print(f'Unknown command!')
    client_socket.close()

main()    
