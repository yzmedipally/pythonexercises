#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config2.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    user = gl.users.list(username='admin_test')[0]
    user_id = user.id
    g_id = gl.groups.search('test-master-group')[0].id
    # add admin user to access repo
    member = gl.group_members.create({'user_id': user_id, 'access_level': gitlab.OWNER_ACCESS }, group_id=g_id)
    # create project
    project = gl.projects.create({'name': 'testex1', 'namespace_id': g_id})
    print "OK"
except ValueError:
    print "ERROR: ", ValueError