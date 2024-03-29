import scratchattach, os

def all_scratchers():
    usernames = []
    for username in usernames:
        yield scratchattach.get_user(username=username)

def find_new_projects():
    for user in all_scratchers():
        newest_project = None