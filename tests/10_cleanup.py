#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config2.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    # delete projects
    project = gl.projects.get('test-master-group/testex1')
    project.delete()
    project = gl.projects.get('exercises00001/testex1')
    project.delete()
    project = gl.projects.get('exercises00002/testex1')
    project.delete()
    project = gl.projects.get('exercises00003/testex1')
    project.delete()
    #delete groups
    g_id = gl.groups.search('test-master-group')[0].id
    gl.groups.delete(g_id)
    g_id = gl.groups.search('exercises00001')[0].id
    gl.groups.delete(g_id)
    g_id = gl.groups.search('exercises00002')[0].id
    gl.groups.delete(g_id)
    g_id = gl.groups.search('exercises00003')[0].id
    gl.groups.delete(g_id)
    #delete users
    user_admin = gl.users.list(username='admin_test')[0]
    user_john = gl.users.list(username='john_test')[0]
    user_peter = gl.users.list(username='peter_test')[0]
    user_thomas = gl.users.list(username='thomas_test')[0]
    user_reviewer = gl.users.list(username='reviewer_test')[0]
    user_latestudent1 = gl.users.list(username='latestudent1_test')[0]
    user_latestudent2 = gl.users.list(username='latestudent2_test')[0]
    
    user_admin.delete()
    user_john.delete()
    user_peter.delete()
    user_thomas.delete()
    user_latestudent1.delete()
    user_latestudent2.delete()
    user_reviewer.delete()
    print "OK"
except ValueError:
    print "ERROR: ", ValueError