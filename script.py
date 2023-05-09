from threading import Thread

def run_comments():
  import comments

t_comments = Thread(target=run_comments)
t_comments.start()
