#!/usr/bin/env python 
import argparse
import json
import sys
from exercisesFunctions import *

def check_config(config):
    configOk = True
    for key in [ "url", "token", "pattern" ]:
        if not key in config:
            print "Config-key %s is not set!" % key
            configOk = False
        elif key == "pattern":
            if len(config["pattern"]) < 4:
                print "Pattern %s is to short (at least 4 chars!)" % \
                    config["pattern"]
                configOk = False
    return configOk

def check_args(action, args):
    if action == "publish" or action == "download":
        if not "exercise" in args:
            raise ValueError("Action %s needs param --exercise!" % action)

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

def dispatch_action(action, config):
    gl = gitlab.Gitlab(config["url"], config["token"]) 
    if action == "check":
        check_action(gl, config)
    elif action == "init":
        init_action(gl, config)
    elif action == "publish": 
        try:
            check_args("publish", args)
        except ValueError as e:
            print str(e)
            return 3
        publish_action(gl)
    elif action == "download":
        try:
            check_args("download", args)
        except ValueError as e:
            print str(e)
            return 3
        download_action(gl)
    elif action == "delete":
        delete_action(gl)
    else:
        print "Action %s unknown (try --help)" % action

def main():
    parser = argparse.ArgumentParser(
            description = 'Exercises - Script to automate gitlab course handling.')
    parser.add_argument(    '--config_file',    
                            default = 'config.json', 
                            required = False, 
                            help = 'Path to config file')
    parser.add_argument(    '--action',
                            default = 'check',
                            required = False,
                            help = """The action to be executed. Possible values:
                            check, init, publish, download, delete""")
    args = parser.parse_args()
    try:
        with open(args.config_file) as config_file:
            config = json.load(config_file)
        config_file.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit(1) 
    if not check_config(config):
        print "Config check failed"
        sys.exit(2)
    dispatch_action(args.action.lower(), config)

if __name__ == "__main__":
    main()
