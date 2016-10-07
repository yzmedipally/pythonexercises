#!/usr/bin/env python 
import argparse
import json
import sys
from exercisesFunctions import *
from pprint import pprint

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

def check_args(args):
    if args.action in ["publish", "download", "add_reviewer"]:
        if not "exercise" in args or args.exercise == None:
            raise ValueError("Action %s needs param --exercise!" % args.action)
    if args.action == "download":
        if not "duedate" in args or args.duedate == None:
            raise ValueError("Action %s needs param --duedate!" % args.action)
    if args.action == "add_reviewer":
        if not "reviewer" in args or args.reviewer == None:
            raise ValueError("Action %s needs param --reviewer!" % args.action)

def check_action(gl, config):
    if check_users(gl, config["students"]):
        print "Users okay!"
    else:
        print "Users not okay!"
    if check_groups(gl, config["students"], config["pattern"]):
        print "Groups okay!" 
    else:
        print "Groups not okay!"
    if check_master_group(gl, config["masterGroup"]):
        print "Master-Group okay!"
    else:
        print "Master-Group not okay!"

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
    print "Successfully created project with config-file"

def publish_action(gl, reviewerString, pattern, exercise): 
    raise NotImplementedError

def dispatch_action(args, config):
    try:
        check_args(args)
    except ValueError as e:
        print str(e)
        sys.exit(3)

    gl = gitlab.Gitlab(config["url"], config["token"])
    action = args.action.lower()

    if   action == "check":
        check_action(gl, config)

    elif action == "init":
        init_action(gl, config)

    elif action == "publish": 
        publish_action(gl)

    elif action == "add_reviewer":
        add_reviewer_to_exercise(
            gl,
            args.reviewer.split(","),
            config["pattern"],
            args.exercise
        )

    elif action == "download":
        download_solutions(gl,
            args.exercise,
            config["pattern"],
            config["downloadDir"],
            args.duedate,
            config["masterGroup"])

    elif action == "delete":
        delete_groups(gl, config["pattern"]) 

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
                            check, init, publish, add_reviewer, download, delete""")
    parser.add_argument(    '--exercise',
                            required = False,
                            help = """The name of the exercise (i.e. the project in gitlab.
                            Required for action publish and download""")
    parser.add_argument(    '--duedate',
                            required = False,
                            help = """The duedate of the exercise. Only used with action download. 
                            at the moment only unixtimestamps are supported""")
    parser.add_argument(    '--reviewer',
                            required = False,
                            help = """Comma separated list of mail addresses of reviewers 
                            for the exercise. Only used with action add_reviewer (or publish?).""")

    args = parser.parse_args()
    try:
        with open(args.config_file) as config_file:
            config = json.load(config_file)
        config_file.close()
    except IOError as e:
        print "Couldn't open {0}: I/O error({1}) - {2}".format(args.config_file, e.errno, e.strerror)
        sys.exit(1) 
    if not check_config(config):
        print "Config check failed"
        sys.exit(2)
    dispatch_action(args, config)

if __name__ == "__main__":
    main()
