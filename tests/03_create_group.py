#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config2.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    group = gl.groups.create({'name': 'test-master-group', 'path': 'test-master-group'})
    print "OK"
except ValueError:
    print "ERROR: ", ValueError
