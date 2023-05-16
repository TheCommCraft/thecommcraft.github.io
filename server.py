import socket, json

s = socket.socket()
s.bind((addr:=socket.gethostbyname(socket.gethostname()), 8000))
s.listen()

with open("server.json", "w") as f:
  json.dump(addr, f)
print(f"IP-address is: {addr}")

message = b"Hi!"

while True:
  client, addr = s.accept()
  client.send(message)
  message = client.recv(2048)
  client.close()
 
