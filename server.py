import socket, json, requests, os

s = socket.socket()
s.bind((addr:=socket.gethostbyname(socket.gethostname()), 8000))
s.listen()

requests.post("db.thecommcraft.repl.co/server.json", cookies={"DB_KEY": os.getenv("DB_KEY")}, data=json.dumps(addr))
print(f"IP-address is: {addr}")

message = b"Hi!"

while True:
  client, addr = s.accept()
  client.send(message)
  message = client.recv(2048)
  client.close()
 
