import scratchattach
from requests import get, post
import time, os, traceback, random, json

if random.random() <= 1.0:
    api = "https://api.scratch.mit.edu"
    session_id = os.getenv("TCC_SESSION_ID")
    x_token = os.getenv("TCC_X_TOKEN")
    session = scratchattach.Session(session_id=session_id, username="TheCommCraft")
    session.xtoken = x_token
    session._headers["X-Token"] = x_token
    user = session.get_linked_user()
    game_s = session.connect_studio(32910287)
    add_projects = [session.connect_project(1047118561)] if random.random() < 0.9 else [i["id"] for i in game_s.projects()] # user.projects() #+ [i["id"] for i in game_s.projects()]
    random.shuffle(add_projects)
    print("Starting as TCC")
else:
    api = "https://api.scratch.mit.edu"
    session_id = os.getenv("UR_SESSION_ID")
    x_token = os.getenv("UR_X_TOKEN")
    session = scratchattach.Session(session_id=session_id, username="-unrelated-")
    session.xtoken = x_token
    session._headers["X-Token"] = x_token
    user = session.get_linked_user()
    game_s = session.connect_studio(32910287)
    add_projects = [session.connect_project(1050606943)] if random.random() < 0.9 else user.projects() #+ [i["id"] for i in game_s.projects()]
    random.shuffle(add_projects)
    print("Starting as ur")
project_1 = session.connect_project(1048568656)

def pc():
    project_1.post_comment(f"You were sent a message! (ID: {random.randrange(1000000)})")

def search(term=None, limit=None):
    url = f"{api}/search/studios?q={term}" if term else f"{api}/search/studios"
    res = get(url).json()
    limit = limit or 1000
    for studio in res[:limit]:
        if not studio["open_to_all"]:
            continue
        yield studio["id"]
        
def connect_all(term=None, limit=None):
    for studio in search(term, limit=limit):
        try:
            studio = session.connect_studio(studio)
            yield studio
        except:
            print(f"Failed to connect to {studio}")

def add_all(term=None, *, projects=None, limit=None):
    projects = projects or add_projects
    for studio in connect_all(term, limit=limit):
        if not studio:
            continue
        if "undertale" in studio.description.lower() or "minecraft" in studio.description.lower():
            continue
        for project in random.sample(projects, 3) if len(projects) > 3 else projects:
            try:
                project = project.id
            except: pass
            try:
                studio.remove_project(project)
                time.sleep(1)
                studio.add_project(project)
                time.sleep(2)
                if random.random() <= 0.02:
                    pc()
                    time.sleep(1)
            except json.decoder.JSONDecodeError:
                print(f"Ratelimited at {studio.id}")
                exit()
            except Exception:
                print(f"Failed to access {studio.id if studio else None}")
                traceback.print_exc()

add_all("non popular projects")
add_all("scratch kat projects", limit=1)
add_all("The Mario and Luigi Gallery", limit=1)
add_all("anything")
add_all("games")
add_all("cool games")
add_all("all projects")
add_all("get this to")
add_all("10000 projects")
add_all("100000 projects")
add_all("everything")
add_all("best games")
add_all("good games")
add_all("whatever")
