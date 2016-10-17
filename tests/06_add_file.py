#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config2.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    project = gl.projects.get('test-master-group/testex1')
    project.files.create({'file_path': 'README.md',
                          'branch_name': 'master',
                          'content': "This is a test file to publish.",
                          'commit_message': 'Create testfile'})
    print "OK"
except ValueError:
    print "ERROR: ", ValueError

