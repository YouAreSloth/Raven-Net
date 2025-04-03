import socket
import threading

class BotConnection:
    def __init__(self, host='0.0.0.0', port=6237):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []
        print(f"Bot ConMan listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, address):
        self.clients.append(client_socket)
        print(f"Bot connected >> {address}")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            print(f"Bot disconnected >> {address}")

    def get_connection_count(self):
        return len(self.clients)

    def start(self):
        print("Bot ConMan starting...")
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_handler.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
            self.disconnect_all_clients()
            self.server_socket.close()
            print("Server stopped")

    def disconnect_all_clients(self):
        for client in self.clients:
            client.close()
        self.clients = []