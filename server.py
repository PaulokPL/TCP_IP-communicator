import socket
import threading

HOST = 'localhost'
PORT = 5001

clients = []


def handle_client(client_socket, addr):
    """
    Funkcja obsługująca połączenie z klientem.
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(4096).decode()
            if message == "file":
                # print(f"[{addr}] {message + 'hej'}")
                file_name = client_socket.recv(1024).decode()
                file_size = int(client_socket.recv(1024).decode())
                file_data = b""
                while len(file_data) < file_size:
                    packet = client_socket.recv(1024)
                    if not packet:
                        break
                    file_data += packet
                with open("received_" + file_name, "wb") as f:
                    f.write(file_data)
                for c in clients:
                    if c != client_socket:
                        mes = "Received new file"
                        c.send(mes.encode())
            elif message:
                print(f"[{addr}] {message}")
                # przesyłanie wiadomości do wszystkich klientów oprócz nadawcy
                for c in clients:
                    if c != client_socket:
                        c.send(message.encode())
            else:
                remove_client(client_socket)
        except:
            remove_client(client_socket)
            break


def remove_client(client_socket):
    """
    Funkcja usuwająca klienta z listy po rozłączeniu.
    """
    clients.remove(client_socket)
    print(f"[DISCONNECTED] {client_socket.getpeername()} disconnected.")


def start_server():
    """
    Funkcja startująca serwer.
    """
    print("[STARTING] Server is starting...")

    # tworzenie gniazda serwera
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        # akceptowanie połączenia
        client_socket, addr = server_socket.accept()

        # tworzenie wątku dla nowego klienta
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == '__main__':
    start_server()