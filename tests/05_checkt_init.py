#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config2.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    user_admin = gl.users.list(username='admin_test')[0]
    user_john = gl.users.list(username='john_test')[0]
    user_peter = gl.users.list(username='peter_test')[0]
    user_thomas = gl.users.list(username='thomas_test')[0]
    user_id_admin = user_admin.id
    user_id_john = user_john.id
    user_id_peter = user_peter.id
    user_id_thomas = user_thomas.id
    
    g_id = gl.groups.search('exercises00001')[0].id
    members = gl.group_members.list(group_id=g_id)
    member_user_ids = []
    for m in members:
        member_user_ids.append(m.id)
    if not user_id_admin in member_user_ids:
        raise "User Admin is missing in Group exercises00001"
    if not user_id_john in member_user_ids:
        raise "User John is missing in Group exercises00001"
    if not user_id_peter in member_user_ids:
        raise "User Peter is missing in Group exercises00001"
    if user_id_thomas in member_user_ids:
        raise "User Thomas should NOT be in Group exercises00001"
    
    g_id = gl.groups.search('exercises00002')[0].id
    members = gl.group_members.list(group_id=g_id)
    member_user_ids = []
    for m in members:
        member_user_ids.append(m.id)
    if not user_id_admin in member_user_ids:
        raise "User Admin is missing in Group exercises00002"
    if not user_id_thomas in member_user_ids:
        raise "User Thomas is missing in Group exercises00002"
    if user_id_john in member_user_ids:
        raise "User John should NOT be in Group exercises00002"
    if user_id_peter in member_user_ids:
        raise "User Peter should NOT be in Group exercises00002"
    print "OK"
except ValueError:
    print "ERROR: ", ValueError
