import socket

# --- НАСТРОЙКИ ---
PASSWORD = "wake_up_sanya"
PORT = 65432

client = None
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', PORT))
    client.sendall(PASSWORD.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print("Статус:", response)
except ConnectionRefusedError:
    print("Служба не активна или компьютер чист.")
finally:
    if client:
        client.close()
