import socket, json, requests, os

s = socket.socket()
s.bind(("0.0.0.0", 8000))
s.listen()

resp = requests.post("https://db.thecommcraft.repl.co/server.json", cookies={"DB_KEY": os.getenv("DB_KEY")}, data=json.dumps(addr:=socket.gethostbyname(socket.gethostname())))
print(resp)
print(f"IP-address is: {addr}")

message = b"Hi!"

while True:
  client, addr = s.accept()
  client.send(message)
  message = client.recv(2048)
  client.close()
 
