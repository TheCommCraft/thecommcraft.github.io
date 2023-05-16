from threading import Thread
import time, os, signal 

def run_comments():
  import comments
def run_server():
  import server

t_comments = Thread(target=run_comments)
t_comments.start()
t_server = Thread(target=run_server)
t_server.start()

time.sleep(1800)
print("Done")
pgid = os.getpgid(os.getpid())
os.killpg(pgid, signal.SIGINT)
