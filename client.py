import socket
import threading
import time


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 65432
client.connect((HOST, PORT))

alias = ""


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if "/ClientName:" in message:
                global alias
                alias = message.split(" ")[-1]
            elif message[-3:] == "ACK":
                print(f"{message} \u2713")  # prints a check mark to acknowledge
            elif alias in message.split(" ")[0]:
                pass
            else:
                print(message)
        except:
            print("An error occurred!\n")
            client.close()
            break


def client_send():
    while True:
        time.sleep(1)
        message = input(f">{alias}:")
        client.send(message.encode("utf-8"))


recieve_thread = threading.Thread(target=client_receive)
recieve_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
