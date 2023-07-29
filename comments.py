import scratchattach, os, time
from threading import Thread
from requests import get
from html import unescape

session_id = os.environ["SESSION"]
username = "StrangeIntensity"

#exit()

session = scratchattach.Session(session_id, username=username)
project = session.connect_project(847888429)
conn = session.connect_cloud(847888429)
client = scratchattach.CloudRequests(conn)

@client.request(name="load")
def load_comments():
  print("loading comments")
  project.update()
  users = {}
  comments_root = get("https://api.scratch.mit.edu/users/TheCommCraft/projects/847888429/comments/?limit=18").json()#project.comments(limit=10)
  comments = []
  for comment in comments_root:
    users[comment['author']['id']] = comment['author']['username']
    comments.append(f"{comment['author']['username']}: {unescape(comment['content'])}")
    comments.extend([(f"        {i['author']['username']}: @{users[i['commentee_id']]} {unescape(i['content'])}", users.__setitem__(i['author']['id'], i['author']['username']))[0] for i in get(f"https://api.scratch.mit.edu/users/TheCommCraft/projects/847888429/comments/{comment['id']}/replies?limit=17").json()])
    if len(comments) >= 18:
        break
  print(comments, comments_root)
  return comments[:18]


print("running server")
client.run(thread=True)




#project = session.connect(824262326)

#project.post_comment(content="WOW")
#print(session.session_id)
