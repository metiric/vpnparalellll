"""
NetGuard Admin Console
Sends shutdown command to local NetGuard service.
"""

import socket

ADMIN_KEY = "wake_up_sanya"
ADMIN_PORT = 65432

client = None
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', ADMIN_PORT))
    client.sendall(ADMIN_KEY.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print("Status:", response)
except ConnectionRefusedError:
    print("Service inactive.")
finally:
    if client:
        client.close()
