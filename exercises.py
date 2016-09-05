#!/usr/bin/env python 
import argparse
import json
from pprint import pprint
from actions import *
import sys

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

def dispatch_action(action):
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

dispatch_action(args.action.lower())
