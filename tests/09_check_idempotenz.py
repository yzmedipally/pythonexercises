#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config2.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    # check users
    user_admin = gl.users.list(username='admin_test')[0]
    user_john = gl.users.list(username='john_test')[0]
    user_peter = gl.users.list(username='peter_test')[0]
    user_thomas = gl.users.list(username='thomas_test')[0]
    user_latestudent1 = gl.users.list(username='latestudent1_test')[0]
    user_latestudent2 = gl.users.list(username='latestudent2_test')[0]
    
    user_id_admin = user_admin.id
    user_id_john = user_john.id
    user_id_peter = user_peter.id
    user_id_thomas = user_thomas.id
    user_id_late_student1 = user_latestudent1.id
    user_id_late_student2 = user_latestudent2.id
    
    g_id = gl.groups.search('exercises00002')[0].id
    members = gl.group_members.list(group_id=g_id)
    member_user_ids = []
    for m in members:
        member_user_ids.append(m.id)
    if not user_id_late_student1 in member_user_ids:
        raise "User Late Student1 is missing in Group exercises00002"
    
    g_id = gl.groups.search('exercises00003')[0].id
    members = gl.group_members.list(group_id=g_id)
    member_user_ids = []
    for m in members:
        member_user_ids.append(m.id)
    if not user_id_late_student2 in member_user_ids:
        raise "User Late Student2 is missing in Group exercises00003"
    
    
    
    # check project files
    project = gl.projects.get('exercises00003/testex1')
    f = project.files.get(file_path='README.md', ref='master')
    if "" <> f.content:
        raise "File in student repository has wrong content!"
    print "OK"
except ValueError:
    print "ERROR: ", ValueError


