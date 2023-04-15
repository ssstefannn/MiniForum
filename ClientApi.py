class ClientApi:
    def __init__(self):
        self.session_id = -1

    # Register the user
    def register_the_user(self, data, client_socket):
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)

    # Login the user
    def login_the_user(self, data, client_socket):
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        try:
            self.session_id = int(response)
        except:
            print(response)

    # Logout the user
    def logout_the_user(self, data, client_socket):
        data = f'{data} {self.session_id}'
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
        session_id = -1

    # Get chat room messages
    def checkout_chat(self, data, client_socket):
        data = f'{data} {self.session_id}'
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response) 

    # Post a message to a chat room
    def post_message(self, data, client_socket):
        data = f'{data} {self.session_id}'
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
