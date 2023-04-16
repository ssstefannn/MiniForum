import requests
import random
from Message import *
from User import *

class Forum:
    def __init__(self):
        self.users = []
        self.messages = []

    def register_the_user(self, arguments, client_socket):
        if len(arguments) != 3:
            response = f'Usage: /register <username> <password>'
            self.send(client_socket, response)
            return
        username = arguments[1]
        password = arguments[2]
        if username in list(map(lambda x: x.username, self.users)):
            response = f'User with username {username} already exists!'
            self.send(client_socket, response)
            return
        self.users.append(User(username, password))
        response = f'Succesfully registered, log in with the /login command!'
        self.send(client_socket, response)
        return

    def login_the_user(self, arguments, client_socket):
        if len(arguments) != 3:
            response = f'Usage: /login <username> <password>'
            self.send(client_socket, response)
            return
        username = arguments[1]
        password = arguments[2]
        user = self.get_user_by_username(username)
        if user == None or user.password != password:
            response = f'Incorrect username or password!'
            self.send(client_socket, response)
            return
        if user.session_id > 0:
            response = f'Already logged in!'
            self.send(client_socket, response)
            return
        session_id = random.randint(1, 100000)
        user.session_id = session_id
        response = str(session_id)
        self.send(client_socket, response)

    # Uses session_id as last argument
    def logout_the_user(self, arguments, client_socket):
        if len(arguments) != 2:
            response = f'Error while trying to log out!'
            self.send(client_socket, response)
            return
        try:
            session_id = int(arguments[1])
        except:
            response = f'Invalid session!'
            self.send(client_socket, response)
            return
        user = self.get_user_by_session_id(session_id)
        if user == None:
            response = f'Invalid session!'
            self.send(client_socket, response)
            return
        user.session_id = 0
        response = f'Successfully logged out!'
        self.send(client_socket, response)
        return

    def checkout_chat(self, arguments, client_socket):
        if len(arguments) != 3:
            response = f'Usage: /checkout_chat <username>|ALL'
            self.send(client_socket, response)
            return
        chat_name = arguments[1]
        try:
            session_id = int(arguments[2])
        except:
            response = f'Invalid session!'
            self.send(client_socket, response)
            return
        user = self.get_user_by_session_id(session_id)
        if user == None:
            response = f'Invalid session!'
            self.send(client_socket, response)
        latest_messages = self.get_latest_messages(user.username, chat_name)
        self.send(client_socket, latest_messages)
        return

    # If one of the usernames is 'ALL' then load the group chat messages        
    def get_latest_messages(self, username1, username2):
        latest_messages = '\n'
        if username1 == 'ALL' or username2 == 'ALL':
            for message in self.messages:
                if message.dst == 'ALL':
                    latest_messages = f'{latest_messages}>>>{message.src}:{message.content}\n'
        else:
            for message in self.messages:
                if message.src == username1\
                and message.dst == username2\
                or message.src == username2\
                and message.dst == username1:
                    latest_messages = f'{latest_messages}>>>{message.src}:{message.content}\n'
        return latest_messages

    # /post_message <username> <content> <session_id>
    def post_message(self, data, client_socket):
        try:
            session_id = int(data.split()[-1])
        except:
            response = f'Invalid session, couldnt parse session_id'
            self.send(client_socket, response)
            return
        user = self.get_user_by_session_id(session_id)
        if user == None:
            response = f'Invalid session, no user with session_id {session_id}'
            self.send(client_socket, response)
            return
        destination = data.split()[1]
        user_destination = None
        if destination != 'ALL':
            user_destination = self.get_user_by_username(destination)
            if user_destination == None:
                response = f'Destination not found!'
                self.send(client_socket, response)
                return
        source = user.username
        content = ' '.join(data.split()[2:-1])
        self.messages.append(Message(source, destination, content))   
        response = f'Successfully posted a message to: {destination}!'
        self.send(client_socket, response)
        return   

    def get_news(self, arguments, client_socket):
        if len(arguments) != 3:
            response = f'Usage: /get_news <topic>'
            self.send(client_socket, response)
            return
        try:
            session_id = int(arguments[2])
        except:
            response = f'Invalid session, couldnt parse session_id'
            self.send(client_socket, response)
            return
        user = self.get_user_by_session_id(session_id)
        if user == None:
            response = f'Invalid session, no user with session_id {session_id}'
            self.send(client_socket, response)
            return
        topic = arguments[1]
        r = requests.get(f'https://newsapi.org/v2/everything?q={topic}&pageSize=5&apiKey=bdc233a737a84cc2bc35d5c06602c0d5', 
                 headers={'Accept': 'application/json'})
        articles = r.json()['articles']
        response = '\n'
        for article in articles:
            response += f'{article["title"]}\n'
            response += f'{article["description"]}\n'
            response += f'Read more at {article["url"]}\n'
            response += f'#############################################\n'
        self.send(client_socket, response)  

    def get_weather(self, arguments, client_socket):
        if len(arguments) != 3:
            response = f'Usage: /get_weather <location>'
            self.send(client_socket, response)
            return
        try:
            session_id = int(arguments[2])
        except:
            response = f'Invalid session, couldnt parse session_id'
            self.send(client_socket, response)
            return
        user = self.get_user_by_session_id(session_id)
        if user == None:
            response = f'Invalid session, no user with session_id {session_id}'
            self.send(client_socket, response)
            return
        location = arguments[1]
        r = requests.get(f'https://api.weatherapi.com/v1/current.json?key=da5747a6435d497e8b3145229231604&q={location}&aqi=no', 
                 headers={'Accept': 'application/json'})
        current = r.json()['current']
        temp = current['temp_c']
        precipitation = current['precip_mm']
        pressure = current['pressure_mb']
        wind = current['wind_kph']
        condition = current['condition']['text']
        response = '\n'
        response += f'Temperature: {temp}°C\n'
        response += f'Precipitation: {precipitation}mm\n'
        response += f'Pressure: {pressure}mbar\n'
        response += f'Wind: {wind}kph\n'
        response += f'Overall: {condition}\n'   
        self.send(client_socket, response)
        return

    # Socket send to reduce boilerplate
    def send(self, client_socket, response):
        client_socket.sendall(response.encode('utf-8'))

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user

    def get_user_by_session_id(self, session_id):
        for user in self.users:
            if user.session_id == session_id:
                return user
