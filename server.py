from constants import *
from utility import Utility
import socket, threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.active_clients = []
        self.active_aliases = []
        self.helper = Utility()
    
    def initialize_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def accept_new_clients(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            client_alias = self.get_client_alias(client_socket)

            if not client_alias:
                self.remove_socket_connection(client_socket)
            
            self.active_aliases.append(client_alias)
            self.active_clients.append(client_socket)
            broadcast_message = self.helper.join_room_message(client_alias)
            formatted_broadcast_message = self.helper.formatted_message_with_alias(SYSTEM_ALIAS, broadcast_message)
            self.broadcast_to_all_clients(formatted_broadcast_message)
            
            thread = threading.Thread(target = self.receive_from_client, args = (client_socket, client_alias))
            thread.start()
    
    def remove_socket_connection(self, client_socket: socket.SocketType, alias: str):
        self.active_clients.remove(client_socket)
        message = self.helper.left_room_message(alias)
        formatted_message = self.helper.formatted_message_with_alias(SYSTEM_ALIAS, message)
        self.broadcast_to_all_clients(formatted_message)
        self.active_aliases.remove(alias)

    def send_message(self, client: socket.SocketType, message: str):
        message = f"{len(message):<{HEADERSIZE}}" + message
        client.send(bytes(message, "utf-8"))
    
    def broadcast_to_all_clients(self, message: str, except_client: socket.SocketType = None):
        for client in self.active_clients:
            if except_client and client != except_client:
                self.send_message(client, message)
            elif not except_client:
                self.send_message(client, message)
        print(message)
    
    def get_client_alias(self, client_socket: socket.SocketType):
        try:
            alias_header = client_socket.recv(HEADERSIZE)
            if not len(alias_header):
                return ""
            alias_length = int(alias_header.decode("utf-8").strip())
            return client_socket.recv(alias_length).decode("utf-8")
        except:
            return ""

    def receive_from_client(self, client_socket: socket.SocketType, alias: str):
        while True:
            try:
                message_header = client_socket.recv(HEADERSIZE)
                
                if not len(message_header):
                    self.remove_socket_connection(client_socket, alias)
                
                message_length = int(message_header.decode("utf-8").strip())
                message_content = client_socket.recv(message_length).decode("utf-8")
                formatted_message = self.helper.formatted_message_with_alias(alias, message_content)
                
                self.broadcast_to_all_clients(formatted_message, client_socket)
            except:
                self.remove_socket_connection(client_socket, alias)
                client_socket.close()
                break

server = Server(SERVER_HOST, SERVER_PORT)
server.initialize_server()
server.accept_new_clients()