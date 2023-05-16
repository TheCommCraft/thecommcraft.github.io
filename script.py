from threading import Thread
import time, os, signal 

print("Running all")

def run_comments():
  print("Running comments...")
  import comments
  print("Run comments.")
def run_server():
  print("Running server...")
  import server
  print("Run server.")

t_comments = Thread(target=run_comments)
t_comments.start()
t_server = Thread(target=run_server)
t_server.start()

time.sleep(10)
print("Done")
pgid = os.getpgid(os.getpid())
os.killpg(pgid, signal.SIGINT)
