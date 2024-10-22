import socket
import threading
from datetime import datetime

# HOST = socket.gethostname()
HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# In-memory Cache
cache = {}

client_count = 0
clients = []
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handleClient(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "exit":
                alias = aliases[clients.index(client)]
                client.send("Disconnected.\n".encode("utf-8"))
                clients.remove(client)
                client.close()
                cache[datetime.now()] = f"{alias} has left the chat."
                broadcast(f"{alias} has left the chat.\n".encode("utf-8"))
                aliases.remove(alias)
                break
            elif message == "status":
                for date, msg in cache:
                    print(f"{str(date)}:     {msg}")
            else:
                cache[datetime.now()] = f"{aliases[clients.index(client)]}: {message}"
                ackmsg = f"{message}ACK\n"
                client.send(ackmsg.encode("utf-8"))
                broadcast(
                    f"{aliases[clients.index(client)]}: {message}".encode("utf-8")
                )
        except:

            alias = aliases[clients.index(client)]
            clients.remove(client)
            client.close()
            cache[datetime.now()] = f"{alias} has left the chat."
            broadcast(f"{alias} has left the chat.\n".encode("utf-8"))
            aliases.remove(alias)
            break


def receive():
    while True:
        print("Receiving and listening")

        client, address = server.accept()
        global client_count
        client_count += 1
        client_name = f"Client{client_count:02d}"

        print(
            f"HOST {HOST} has established connection with {client_name}:{str(address)} at {datetime.now()}"
        )

        alias = client_name
        aliases.append(alias)
        clients.append(client)
        if len(clients) > 3:
            client.close()
            return
        client.send(f"/ClientName: {client_name}\n".encode("utf-8"))
        cache[datetime.now()] = f"{alias} has joined the chat!"
        client.send(f"Connected to the server as {alias}\n".encode("utf-8"))
        broadcast(f"{alias} has joined the chat!\n".encode("utf-8"))

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
