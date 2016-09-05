from exercisesFunctions import *
def check_action(gl, config):
    if check_users(gl, config["students"]):
        print "Users okay!"
    else:
        print "Users not okay!"
    if check_groups(gl, config["students"], config["pattern"]):
        print "Groups okay!" 
    else:
        print "Groups not okay"

def init_action(gl, config):
    if not "adminMails" in config:
        config["adminMails"] = []
    try:
        init_groups(
            gl,
            config["students"],
            config["pattern"],
            config["adminMails"]
        ) 
    except ValueError as e:
        pprint(e)

def publish_action(gl):
    raise NotImplementedError

def download_action(gl):
    raise NotImplementedError

def delete_action(gl):
    delete_groups(gl, config["pattern"]) 

