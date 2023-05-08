import scratchattach, os

password = os.environ["SESSION"]
username = "StrangeIntensity"

session = scratchattach.login(username, password)

project = session.connect_project(824262326)

#project.post_comment(content="Nice!")
