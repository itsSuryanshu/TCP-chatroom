import socket
import threading
from datetime import datetime
import time

# HOST = socket.gethostname()
HOST = "127.0.0.1"
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# In-memory Cache
cache = {}

# keep track of number of connections made, so that clients can be named in order that they join
client_count = 0
# store clients in a list, and names them using client_count
clients = []
aliases = []


# function that sends a message to all clients connected to the server
def broadcast(message):
    for client in clients:
        client.send(f"{message}".encode("utf-8"))


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
                broadcast(f"\n---{alias} has left the chat.---\n")
                aliases.remove(alias)
                break
            elif message == "status":
                for date, msg in cache.items():
                    client.send(f"{str(date)}:     {msg}".encode("utf-8"))
            else:
                cache[datetime.now()] = f"{aliases[clients.index(client)]}: {message}"
                ackmsg = f"Server> {message}ACK"
                client.send(ackmsg.encode("utf-8"))
                time.sleep(1)
                broadcast(f"{aliases[clients.index(client)]}: {message}")
        except:

            alias = aliases[clients.index(client)]
            clients.remove(client)
            client.close()
            cache[datetime.now()] = f"{alias} has left the chat."
            broadcast(f"\n---{alias} has left the chat.---\n")
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

        aliases.append(client_name)
        clients.append(client)
        if len(clients) > 3:
            client.close()
            return
        client.send(f"Server> /ClientName: {client_name}".encode("utf-8"))
        cache[datetime.now()] = f"{client_name} has joined the chat!"
        client.send(f"Server> Connected to the server as {client_name}".encode("utf-8"))
        time.sleep(1)
        broadcast(f"\n---{client_name} has joined the chat!---\n")

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
