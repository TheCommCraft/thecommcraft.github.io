from threading import Thread
import time, sys

def run_comments():
  import comments

t_comments = Thread(target=run_comments)
t_comments.start()

time.sleep(1800)
sys.exit("Done")
