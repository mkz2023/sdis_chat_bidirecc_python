import socket
import threading

# Función para manejar la recepción de mensajes del cliente
def handle_client(client_socket, client_address):
    print(f"Conexión aceptada desde {client_address}")

    while True:
        try:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if not data:
                print(f"Cliente {client_address} desconectado.")
                break
            print(f"\nClient: {data.decode()}")

            # Reenviar el mensaje a todos los clientes conectados, excepto al cliente que envió el mensaje
            broadcast(data, client_socket)
        except:
            print(f"Error al recibir datos del cliente {client_address}.")
            break

    client_socket.close()

# Función para reenviar mensajes a todos los clientes
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message)

# Función para enviar mensajes desde el servidor a los clientes
def send_message_to_clients():
    while True:
        try:
            message = input("Server: ")
            broadcast(message.encode(), None)  # Pass None as sender_socket
        except KeyboardInterrupt:
            break

# Configuración del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9999))
server_socket.listen(5)

print("Servidor de chat iniciado. Esperando conexiones...")

clients = []

# Iniciar un hilo para enviar mensajes desde el servidor a los clientes
send_thread = threading.Thread(target=send_message_to_clients)
send_thread.start()

while True:
    # Esperar a que lleguen las conexiones
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)

    # Iniciar un nuevo hilo para manejar el cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
