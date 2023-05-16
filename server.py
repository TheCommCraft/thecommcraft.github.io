import socket

s = socket.socket()
s.bind((socket.gethostbyname(socket.gethostname()), 8000))
s.listen()

message = b"Hi!"

while True:
  client, addr = s.accept()
  client.send(message)
  message = client.recv(2048)
  client.close()
 
