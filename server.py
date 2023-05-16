import socket, json, requests, os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8080))
s.listen()

resp = requests.post("https://db.thecommcraft.repl.co/server.json", cookies={"DB_KEY": os.getenv("DB_KEY")}, data=json.dumps(addr:=socket.gethostbyname(socket.gethostname())))
print(resp)
print(f"IP-address is: {addr}")

message = b"Hi!"

while True:
  client, addr = s.accept()
  print(addr)
  client.send(message)
  
  message = client.recv(2048)
  print(message)
  client.close()
 
