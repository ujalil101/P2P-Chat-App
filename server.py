import socket
import threading
import datetime

def handle_client(client_socket, client_address, username):
    print(f"Accepted connection from {client_address} as {username}")
    while True:
        try:
            # recieve message from client
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"{username}: {message}")
                # send message to all clients
                broadcast_message(f"{username}: {message}", client_socket)
            else:
                # close connection
                close_connection(client_socket, client_address)
                break
        except ConnectionResetError:
            close_connection(client_socket, client_address)
            break


def broadcast_message(message, sender_socket):
    # send message to all clients except the sender
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode("utf-8"))
            except:
                # if sending message fails, close the connection
                client.close()
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def close_connection(client_socket, client_address):
    print(f"Connection closed with {client_address}")
    remove_client(client_socket)
    client_socket.close()

def run_server():
    server_ip = "127.0.0.1"
    port = 8000

    # create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, port))
    server.listen(5)
    print(f"Listening on {server_ip}:{port}")

    while True:
        # accept incoming connections
        client_socket, client_address = server.accept()
        clients.append(client_socket)

        # receive username from the client
        username = client_socket.recv(1024).decode("utf-8")

        # start new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, username))
        client_thread.start()


clients = []

if __name__ == "__main__":
    run_server()