#!/usr/bin/env python
import json
import gitlab

# read config file
config_file = open("test/test_config1.json", "r")
config = json.load(config_file)
config_file.close()

gl = gitlab.Gitlab(config["url"], config["token"])

try:
    # create test users in gitlab
    user = gl.users.create({'email': 'admin.test@tum.de', \
                        'password': 's3cur3s3cr3T', \
                        'username': 'admin_test', \
                        'name': 'Admin Test'})

    user = gl.users.create({'email': 'john.test@tum.de', \
                        'password': 's3cur3s3cr3V', \
                        'username': 'john_test', \
                        'name': 'John Test'})

    user = gl.users.create({'email': 'peter.test@tum.de', \
                        'password': 's3cur3s3cr3S', \
                        'username': 'peter_test', \
                        'name': 'Peter Test'})

    user = gl.users.create({'email': 'thomas.test@tum.de', \
                        'password': 's3cur3s3cr3Y', \
                        'username': 'thomas_test', \
                        'name': 'Thomas Test'})

    user = gl.users.create({'email': 'reviewer.test@tum.de', \
                        'password': 's3cur3s3cr3R', \
                        'username': 'reviewer_test', \
                        'name': 'Reviewer Test'})
    print "OK"
except ValueError:
    print "ERROR: ", ValueError
