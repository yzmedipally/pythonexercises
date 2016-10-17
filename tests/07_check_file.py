#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config2.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    # delete project
    project = gl.projects.get('exercises00001/testex1')
    f = project.files.get(file_path='README.md', ref='master')
    if "" <> f.content:
        raise "File in student repository has wrong content!"
    project = gl.projects.get('exercises00002/testex1')
    f = project.files.get(file_path='README.md', ref='master')
    if "" <> f.content:
        raise "File in student repository has wrong content!"
    print "OK"
except ValueError:
    print "ERROR: ", ValueError


