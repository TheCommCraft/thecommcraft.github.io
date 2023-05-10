import scratchattach, os, time

session_id = os.environ["SESSION"]
username = "StrangeIntensity"

exit()

session = scratchattach.Session(session_id, username=username)
project = session.connect_project(847888429)
conn = session.connect_cloud(847888429)
client = scratchattach.CloudRequests(conn)

@client.request(name="load")
def load_comments():
  print("loading comments")
  project.update()
  comments_root = project.comments(limit=10)
  comments = []
  for comment in comments_root:
    comments.append(f"{comment['author']['username']}: {comment['content']}")
    comments.extend([f"   {i['author']['username']}: @{comment['author']['username']} {i['content']}" for i in project.get_comment_replies(comment_id=comment["id"], limit=10)])
    if len(comments) > 10:
        break
  print(comments, comments_root)
  return comments[:10]


print("running server")
client.run(thread=True)
time.sleep(1800)
exit()
#project = session.connect_project(824262326)

#project.post_comment(content="WOW")
#print(session.session_id)
