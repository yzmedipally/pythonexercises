#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test_config.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    # create additional test users in gitlab
    user = gl.users.create({'email': 'latestudent1.test@tum.de', \
                        'password': 's3cur3s3cr3W', \
                        'username': 'latestudent1_test', \
                        'name': 'Latestudent1 Test'})

    user = gl.users.create({'email': 'latestudent2.test@tum.de', \
                        'password': 's3cur3s3cr3X', \
                        'username': 'latestudent2_test', \
                        'name': 'Latestudent2 Test'})
    print "OK"
except ValueError:
    print "ERROR: ", ValueError
