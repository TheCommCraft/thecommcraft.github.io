import scratchattach, os

session_id = os.environ["SESSION"]
username = "StrangeIntensity"

session = scratchattach.Session(session_id, username=username)

project = session.connect_project(824262326)

project.post_comment(content="Nice!")
