import scratchattach, os, requests, time

LENGTH = 60 * 30

commented = set()

old_get = requests.get
old_post = requests.post
old_put = requests.put

def get(*args, **kwargs):
    if "mit.edu" in args[0]:
        time.sleep(1)
    return old_get(*args, **kwargs)

def post(*args, **kwargs):
    if "scratch" in args[0]:
        time.sleep(1)
    return old_post(*args, **kwargs)

def put(*args, **kwargs):
    if "scratch" in args[0]:
        time.sleep(1)
    return old_put(*args, **kwargs)

requests.get = get
requests.post = post
requests.put = put

def acquire_session():
    st = os.getenv("st") # session token
    xt = os.getenv("xt") # Xtoken
    un = os.getenv("un") # username
    session = scratchattach.Session(st, username=un)
    if session.xtoken = "":
        session.xtoken = xt
        session._headers["X-Token"] = xt
    return session

def all_scratchers():
    usernames = ["yoshihome", "philhub"]
    for username in usernames:
        yield scratchattach.get_user(username=username)

def find_new_projects():
    for user in all_scratchers():
        newest_project = user.projects(limit=1)[0]
        newest_project.update()
        if newest_project.views > 10:
            break
        if newest_project.id in commented:
            break
        yield (newest_project.id, newest_project.author)
        commented.add(newest_project.id)

def choose_comment(__id, author):
    comments = ["Great job with this game, {}!", "You really outdid yourself with this one, {}.", "I like this. I can't stop playing this. Cool, {}!", "{}, this is great!", "Great! I expect this to become popular, {}.", "You have a skill, {}!"]
    return comments[hash((__id, "what"))%len(comments)].format(author)

def comment_all():
    for proj, author in find_new_projects():
        comment = choose_comment(proj, author)
        session = acquire_session()
        project = session.connect_project(proj)
        project.post_comment(comment)
        project.love()
        print("commented '{c}' on project {pn}({pid}) by {a}".format(c=comment, pn=project.title, pid=project.id, a=author))

start_time = time.time()
end_time = start_time + LENGTH

print("starting at", start_time, "and running til",  end_time)

while time.time() <= end_time:
    next_time = time.time() + 10
    comment_all()
    time.sleep(max(0, next_time - time.time()))

print("done at", time.time())
    