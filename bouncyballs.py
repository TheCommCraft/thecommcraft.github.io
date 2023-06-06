from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from threading import Thread
import os, time, random, requests
from scratchattach import Session, CloudRequests, TwCloudRequests, CloudEvents

class UnknownUserError(Exception):
  pass

class UnknownLevelError(Exception):
  pass

password = os.getenv("MONGO_DB_KEY")
session_id = os.getenv("SESSION")

uri = f"mongodb+srv://TheCommCraft:{password}@bouncyballscluster.cdqbnlp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
mongoclient = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
mongoclient.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")

db = mongoclient["maindatabase"]
users = db["users"]
levels = db["levels"]
logs = db["logs"]

session = Session(session_id, username="StrangeIntensity")
conn = session.connect_cloud(856420361)
proj = session.connect_project(856420361)

events = CloudEvents(856420361)
          
client = CloudRequests(conn, used_cloud_vars=["1", "2", "3"])

'''@events.event
def on_set(event): #Called when a cloud var is set
    print(f"{event.user} set the variable {event.var} to the valuee {event.value} at {event.timestamp}")'''

#events.start(thread=True)

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def find_user(username):
  user = users.find_one({"username": username})
  if user is None:
    raise UnknownUserError
  return user
    
def update_user(username, newvalues):
    users.update_one({"username": username}, {"$set": newvalues})

def create_user(username):
  users.insert_one(user:={"owns": [], "can_edit": [], "username": username})
  return user

def find_level(levelid):
  level = levels.find_one({"level_id": levelid})
  if level is None:
    raise UnknownLevelError
  return level
    
def update_level(levelid, _set=None, _inc=None):
    _set = {} if _set is None else _set
    _inc = {} if _inc is None else _inc
    levels.update_one({"level_id": levelid}, {"$set": _set, "$inc": _inc})

def create_level(levelid):
  levels.insert_one(level:={"level_id": levelid})
  return level

def random_level():
  return random.choice(levels.find())
  
def find_ran_levels(amount=20):
  return random.sample((result:=list(levels.find())), min(len(result), amount))

def find_pop_levels():
  return_levels = find_ran_levels(100)
  return_levels = list(sorted(return_levels, key = lambda x: x.get("views", 0), reverse=True))[:20]
  return return_levels

def find_levels():
  return random.sample((lev_set:=list(set((hashabledict(i) for i in find_ran_levels() + find_pop_levels())))), min(20, len(lev_set)))

def get_comments():
  return requests.get("https://api.scratch.mit.edu/users/TheseCommCraft/projects/856420361/comments").json()

@client.event
def on_request(request):
  print("Received request")

@client.request(name="savelevel")
def save_level(level_id, level_name, *level_content):
  level_content = "&".join(level_content)
  username = client.get_requester()
  try:
    user = find_user(username)
  except UnknownUserError:
    user = create_user(username)
  try:
    level = find_level(level_id)
  except UnknownLevelError:
    level = create_level(level_id)
  if level.get("creator", username) != username:
    return "error"
  if level_name == "comments":
    try:
      level_name = list(filter(lambda x: x["author"]["username"] == username, get_comments()))[0]["content"]
    except:
      return "No comment"
  newvalues = {"content": level_content, "name": level_name, "creator": username}
  if level_name == "Nothing":
    newvalues.pop("name")
  if level_content == "":
    newvalues.pop("content")
  if "creator" in level:
    newvalues.pop("creator")
  else:
    update_user(username, {"owns": user.get("owns", []) + [level_id], "can_edit": user.get("can_edit", []) + [level_id]})
  update_level(level_id, newvalues)
  return "success"

@client.request(name="loadlevel")
def load_level(level_id):
  level = find_level(level_id)
  level_content = level["content"]
  if time.time() - client.get_timestamp() < 10:
    update_level(level_id, _inc={"views": 1})
  #tabs.update_one({"tab": "popular"}, {"$set": {"content": sorted(tabs.find_one({"tab": "popular"})["content"] + [level_id], key=lambda x: find_level(x)["views"], reversed=True)}})
  return level_content

@client.request(name="loadlevels")
def load_levels():
  found_levels = find_levels()
  return_levels = []
  [return_levels.extend((i.get("level_id", "0"), i.get("name", "levelName"), i.get("creator", "aHacker"), str(i.get("views", "0")), "", "", "")) for i in found_levels]
  return return_levels

client.run(thread=True)
