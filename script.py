from threading import Thread
import time, os, signal 

def run_comments():
  import comments

t_comments = Thread(target=run_comments)
t_comments.start()

time.sleep(180)
print("Done")
pgid = os.getpgid(os.getpid())
os.killpg(pgid, signal.SIGTERM)
