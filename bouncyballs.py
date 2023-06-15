from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from threading import Thread
import os, time, random, requests, signal
from scratchattach import Session, CloudRequests, TwCloudRequests, CloudEvents, WsCloudEvents, get_cloud_logs, TwCloudConnection

"""
def _update(self):
    while True:
        try:
            data = self.connection.websocket.recv().split('\n')
            result = []
            for i in data:
                try:
                    result.append(json.loads(i))
                except Exception:
                    pass
            for activity in result:
                if "on_"+activity["method"] in self._events:
                    self._events["on_"+activity["method"]](self.Event(user=None, var=activity["name"][2:], name=activity["name"][2:], value=activity["value"], timestamp=time.time()*10000))
        except Exception:
            try:
                while True: 
                    self.connection._connect(cloud_host=self.connection.cloud_host)
                    self.connection._handshake()
                    try:
                        data = self.connection.websocket.recv().split('\n')
                        break
                    except Exception as e:
                        print(f"problem 1: {e}")
            except Exception as e:
                print(f"problem 2: {e}")
                if "on_disconnect" in self._events:
                    self._events["on_disconnect"]()
                    
WsCloudEvents._update = _update
"""

class UnknownUserError(Exception):
  pass

class UnknownLevelError(Exception):
  pass

def get_real_timestamp(test=False):
  if test==False:
    logs = get_cloud_logs(client.project_id, filter_by_var_named="TO_HOST")
    activity = list(filter(lambda x : "."+client.last_request_id in x["value"], logs))
    if len(activity) > 0:
        return activity[0]["timestamp"]
  logs = get_cloud_logs(clienttest.project_id, filter_by_var_named="TO_HOST")
  activity = list(filter(lambda x : "."+clienttest.last_request_id in x["value"], logs))
  if len(activity) > 0:
      return activity[0]["timestamp"]

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
conntest = session.connect_cloud(856420361)
twconntest = TwCloudConnection(project_id=856420361, username="player1000")
conn = session.connect_cloud(854229895)
twconn = TwCloudConnection(project_id=854229895, username="player1000")

"""
_last_timestamp = 0

def last_timestamp(self):
  global _last_timestamp
  return _last_timestamp
def set_last_timestamp(self, timestamp):
  global _last_timestamp
  _last_timestamp = timestamp
  #print(f"self.ws_data is {getattr(self, 'ws_data', 'not existing')}")
  #print(f"Set timestamp to {timestamp}")

CloudRequests.last_timestamp = property(last_timestamp)
CloudRequests.last_timestamp = CloudRequests.last_timestamp.setter(set_last_timestamp)
"""

client = CloudRequests(conn, used_cloud_vars=["1", "2", "3"])
twclient = TwCloudRequests(twconn, used_cloud_vars=["1", "2", "3"])
clienttest = CloudRequests(conntest, used_cloud_vars=["1", "2", "3"])
twclienttest = TwCloudRequests(twconntest, used_cloud_vars=["1", "2", "3"])

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
  return random.choice(levels.find({"$or": [{"public": {"$exists": False}}, {"public": True}]}))
  
def find_ran_levels(amount=20):
  return random.sample((result:=list(levels.find({"$or": [{"public": {"$exists": False}}, {"public": True}]}))), min(len(result), amount))

def find_pop_levels():
  return_levels = find_ran_levels(100)
  return_levels = list(sorted(return_levels, key = lambda x: x.get("views", 0), reverse=True))[:20]
  return return_levels

def find_levels():
  return random.sample((lev_set:=list(set((hashabledict(i) for i in find_ran_levels() + find_pop_levels())))), min(20, len(lev_set)))

def get_comments(pid=854229895):
  return requests.get("https://api.scratch.mit.edu/users/TheseCommCraft/projects/{pid}/comments").json()

#@client.event
def on_request(request):
  print("Received request")

@client.request(name="savelevel")
def save_level(level_id, level_name, *level_content):
  if time.time() - get_real_timestamp() / 1000 > 20:
    return
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

@twclient.request(name="savelevel")
def save_level(level_id, level_name, *level_content):
  return "Uploading from TurboWarp doesn't work"

@client.request(name="loadlevel")
def load_level(level_id):
  if time.time() - get_real_timestamp() / 1000 > 20:
    return
  print(f"Finding level {level_id}...")
  level = find_level(level_id)
  level_content = level["content"]
  update_level(level_id, _inc={"views": 1})
  #tabs.update_one({"tab": "popular"}, {"$set": {"content": sorted(tabs.find_one({"tab": "popular"})["content"] + [level_id], key=lambda x: find_level(x)["views"], reversed=True)}})
  return level_content

@twclient.request(name="loadlevel")
def load_level(level_id):
  if time.time() - get_real_timestamp() / 1000 > 20:
    return
  print(f"Finding level {level_id}...")
  level = find_level(level_id)
  level_content = level["content"]
  update_level(level_id, _inc={"views": 1})
  #tabs.update_one({"tab": "popular"}, {"$set": {"content": sorted(tabs.find_one({"tab": "popular"})["content"] + [level_id], key=lambda x: find_level(x)["views"], reversed=True)}})
  return level_content

@client.request(name="loadlevels")
def load_levels():
  if time.time() - get_real_timestamp() / 1000 > 20:
    return
  found_levels = find_levels()
  return_levels = []
  [return_levels.extend((i.get("level_id", "0"), i.get("name", "levelName"), i.get("creator", "aHacker"), str(i.get("views", "0")), "", "", "")) for i in found_levels]
  return return_levels

@twclient.request(name="loadlevels")
def load_levels():
  if time.time() - get_real_timestamp() / 1000 > 20:
    return
  found_levels = find_levels()
  return_levels = []
  [return_levels.extend((i.get("level_id", "0"), i.get("name", "levelName"), i.get("creator", "aHacker"), str(i.get("views", "0")), "", "", "")) for i in found_levels]
  return return_levels

@clienttest.request(name="savelevel")
def save_level(level_id, level_name, *level_content):
  if time.time() - get_real_timestamp(True) / 1000 > 20:
    return
  level_content = "&".join(level_content)
  username = clienttest.get_requester()
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
      level_name = list(filter(lambda x: x["author"]["username"] == username, get_comments(856420361)))[0]["content"]
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

@twclienttest.request(name="savelevel")
def save_level(level_id, level_name, *level_content):
  return "Uploading from TurboWarp doesn't work"

@clienttest.request(name="loadlevel")
def load_level(level_id):
  if time.time() - get_real_timestamp(True) / 1000 > 20:
    return
  print(f"Finding level {level_id}...")
  level = find_level(level_id)
  level_content = level["content"]
  update_level(level_id, _inc={"views": 1})
  #tabs.update_one({"tab": "popular"}, {"$set": {"content": sorted(tabs.find_one({"tab": "popular"})["content"] + [level_id], key=lambda x: find_level(x)["views"], reversed=True)}})
  return level_content

@twclienttest.request(name="loadlevel")
def load_level(level_id):
  if time.time() - get_real_timestamp() / 1000 > 20:
    return
  print(f"Finding level {level_id}...")
  level = find_level(level_id)
  level_content = level["content"]
  update_level(level_id, _inc={"views": 1})
  #tabs.update_one({"tab": "popular"}, {"$set": {"content": sorted(tabs.find_one({"tab": "popular"})["content"] + [level_id], key=lambda x: find_level(x)["views"], reversed=True)}})
  return level_content

@clienttest.request(name="loadlevels")
def load_levels():
  if time.time() - get_real_timestamp(True) / 1000 > 20:
    return
  found_levels = find_levels()
  return_levels = []
  [return_levels.extend((i.get("level_id", "0"), i.get("name", "levelName"), i.get("creator", "aHacker"), str(i.get("views", "0")), "", "", "")) for i in found_levels]
  return return_levels

@twclienttest.request(name="loadlevels")
def load_levels():
  if time.time() - get_real_timestamp() / 1000 > 20:
    return
  found_levels = find_levels()
  return_levels = []
  [return_levels.extend((i.get("level_id", "0"), i.get("name", "levelName"), i.get("creator", "aHacker"), str(i.get("views", "0")), "", "", "")) for i in found_levels]
  return return_levels

"""
client.add_request(save_level, name="savelevel")
client.add_reqeust(load_level, name="loadlevel")
client.add_reqeust(load_levels, name="loadlevels")

clienttest.add_request(save_level, name="savelevel")
clienttest.add_reqeust(load_level, name="loadlevel")
clienttest.add_reqeust(load_levels, name="loadlevels")
"""

client.run(thread=True)
clienttest.run(thread=True)
twclient.run(thread=True)
twclienttest.run(thread=True)
time.sleep(1800)
print("Done")
pgid = os.getpgid(os.getpid())
os.killpg(pgid, signal.SIGINT)
