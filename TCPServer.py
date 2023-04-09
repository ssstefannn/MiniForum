import requests
import socket
import random

def test_news_api():
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=bdc233a737a84cc2bc35d5c06602c0d5', 
                 headers={'Accept': 'application/json'})
    articles = r.json()["articles"]
    for article in articles:
        print(article["title"])

def register_the_user(arguments, client_socket):
    if len(arguments) != 3:
        response = f'Usage: /register <username> <password>'
        send(client_socket, response)
        return
    username = arguments[1]
    password = arguments[2]
    if username in users:
        response = f'User with username {username} already exists!'
        send(client_socket, response)
        return
    
    users.append(User(username, password))
    set_user_password(username, password)

    response = f'Succesfully registered, log in with the /login command!'
    send(client_socket, response)
    return

def login_the_user(arguments, client_socket):
    if len(arguments) != 3:
        response = f'Usage: /login <username> <password>'
        send(client_socket, response)
        return
    username = arguments[1]
    password = arguments[2]
    if username not in list(map(lambda x: x.username, users)) or get_user_password(username) != password:
        response = f'Incorrect username or password!'
        send(client_socket, response)
        return
    if get_session_id(username) > 0:
        response = f'Already logged in!'
        send(client_socket, response)
        return
    session_id = random.randint(1, 100000)
    set_session_id(username, session_id)
    response = str(session_id)
    send(client_socket, response)

def logout_the_user(arguments, client_socket):
    if len(arguments) != 2:
        response = f'Error while trying to log out!'
        send(client_socket, response)
        return
    session_id = int(arguments[1])
    
    for user in users:
        if user.session_id == session_id:
            user.session_id = 0
            response = f'Successfully logged out!'
            send(client_socket, response)
            return

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session_id = 0

def send(client_socket, response):
    client_socket.sendall(response.encode('utf-8'))

def get_user_password(username):
    for user in users:
        if user.username == username:
            return user.password

def set_user_password(username, password):
    for user in users:
        if user.username == username:
            user.password = password

def get_session_id(username):
    for user in users:
        if user.username == username:
            return user.session_id

def set_session_id(username, session_id):
    for user in users:
        if user.username == username:
            user.session_id = session_id

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 6666))
server_socket.listen(1)
print('Server listening on port 6666...')

users = []

while True:
    client_socket, address = server_socket.accept()
    print(f'Connection from {address} established.')
    data = client_socket.recv(1024).decode('utf-8')
    print(f'Received data: {data}')
    # response = 'Hello, client!'
    # client_socket.sendall(response.encode('utf-8'))
    if data[0] == '/':
        arguments = data.split()
        command = arguments[0]
        if command == '/register':
            #register the user;
            register_the_user(arguments, client_socket)
        elif command == '/login':
            #log in the user
            login_the_user(arguments, client_socket)
        elif command == '/logout':
            #log out the user
            logout_the_user(arguments, client_socket)
        elif command == '/weather':
            # get the current weather
            x = 0
        elif command == '/news':
            # get the news feed
            x = 0
        elif command == '/chatall': 
            # chat with everyone
            x = 0
        elif command == '/chat':
            # chat with a particular user
            x = 0
        else:
            response = f'Unknown command {command}'
            client_socket.sendall(response.encode('utf-8'))
    client_socket.close()
