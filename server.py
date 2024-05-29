import socket
import pickle
import random

HOST = '127.0.0.1'
PORT = 8088


sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, _ = sock.accept()

p, g, A = pickle.loads(conn.recv(1024))

b = random.randint(2, 10)
B = (g ** b) % p
conn.send(pickle.dumps(B))

K = (A ** b) % p

encrypted_message = conn.recv(1024).decode()
decrypted_message = ''.join([chr(ord(char) - K) for char in encrypted_message])
print("Сообщение клиента:", decrypted_message)

response = "Привет, клиент!"
encrypted_response = ''.join([chr(ord(char) + K) for char in response])
conn.send(encrypted_response.encode())

conn.close()
