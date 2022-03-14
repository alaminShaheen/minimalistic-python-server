from constants import *
from utility import Utility
import socket, threading, sys

class Client:
    def __init__(self):
        self.helper = Utility()

    def initialize_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))
        self.alias = input("What should we call u? - ")
        self.send_message(self.alias)

    def receive_from_server(self, _):
        while True:
            while True:
                try:
                    message_header = self.client_socket.recv(HEADERSIZE)
                    message_length = int(message_header.decode("utf-8").strip())
                    message_content = self.client_socket.recv(message_length).decode("utf-8")
                    # formatted_message = self.helper.formatted_message_with_alias(self.alias, message_content)
                    print(message_content)
                except:
                    continue

    def send_message(self, message: str):
        message = f"{len(message):<{HEADERSIZE}}" + message
        self.client_socket.send(bytes(message, "utf-8"))
    
    def send_to_server(self, _):
        while True:
            message = sys.stdin.readline()
            self.send_message(message)
            print ("\033[A\033[A")
            sys.stdout.write("<You>: ")
            sys.stdout.write(message)
            sys.stdout.flush()

client_server = Client()
client_server.initialize_server()

send_thread = threading.Thread(target = client_server.send_to_server, args = (client_server.client_socket,))
send_thread.start()

receive_thread = threading.Thread(target = client_server.receive_from_server, args = (client_server.client_socket,))
receive_thread.start()


            
    
