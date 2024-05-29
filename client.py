import socket
import pickle
import random
import os

HOST = '127.0.0.1'
PORT = 8088

# Load or generate p, g, a from a file
if os.path.exists('client_public_key.txt'):
    with open('client_public_key.txt', 'r') as file:
        p, g, a = map(int, file.readline().split())
else:
    p, g, a = random.randint(2, 73), random.randint(2, 73), random.randint(2, 10)
    with open('client_public_key.txt', 'w') as file:
        file.write(f"{p} {g} {a}")

sock = socket.socket()
sock.connect((HOST, PORT))

A = (g ** a) % p
sock.send(pickle.dumps((p, g, A)))

B = pickle.loads(sock.recv(1024))

K = (B ** a) % p
print("Calculated client key:", K)

message = "Hello, server!"
encrypted_message = ''.join([chr(ord(char) + K) for char in message])
print(f"Encrypted message: {encrypted_message}")
sock.send(encrypted_message.encode())

encrypted_response = sock.recv(1024).decode()
decrypted_response = ''.join([chr(ord(char) - K) for char in encrypted_response])
print("Server's response:", decrypted_response)

sock.close()
