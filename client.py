import socket
import threading

# Función para manejar la recepción de mensajes del servidor
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith("Server: "):
                print(message)
            else:
                print(f"Client: {message}")
        except:
            print("¡Error! Conexión perdida con el servidor.")
            client_socket.close()
            break

# Configuración del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9999))

# Iniciar un hilo para recibir mensajes del servidor
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Enviar mensajes al servidor
while True:
    try:
        message = input()
        client_socket.send(message.encode())
    except KeyboardInterrupt:
        print("¡Adiós!")
        client_socket.close()
        break
