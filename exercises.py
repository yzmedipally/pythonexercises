#!/usr/bin/env python 
import argparse
import requests
import json
import pprint

def further_arg_checking( ):
    "This checks the given cli-args depending on the given action"
    if args.action == "create-groups" or "remove-course":
        if not args.pattern:
            parser.error('--pattern has to be given if action is' +  args.action)
    if args.action == "create-groups":
        if not args.number: 
            parser.error('--number has to be given if action is' +  args.action)
    return

def parse_search_req(json, parse_for):
    for item in json:
        yield(item[parse_for])

def send_request_to_gitlab( ):
    "This encapsulates the requests sent to gitlab" 
    if args.action == "create-groups":
        resp = requests.post('https://gitlab.lrz.de/api/v3/groups?name=' + args.pattern + '&path=' + args.pattern, headers={'PRIVATE-TOKEN':args.token}) 
    if args.action == "remove-course":
        resp = requests.get('https://gitlab.lrz.de/api/v3/groups?search=' + args.pattern, headers={'PRIVATE-TOKEN':args.token}) 
        ids = parse_search_req(resp.json(), "id")
        print(ids)
#        resp = requests.delete('https://gitlab.lrz.de/api/v3/projects/' + args.pattern, headers={'PRIVATE-TOKEN':args.token})  
    else:
        print("Unknown action")

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(resp)

    if resp.status_code != 200: 
        print(resp)

    print json.dumps(resp.json(), indent=2, sort_keys=True)

parser = argparse.ArgumentParser(description = 'Exercises - Script to automate gitlab course handling.')
parser.add_argument('token',
        help = 'gitlab Auth-Token')
parser.add_argument('action',
        help = 'The action to be executed. Possible values: create-group, get-solutions...')
parser.add_argument('--pattern',
        help = 'Pattern for exercise groups (will be extended with numerical IDs)')            
parser.add_argument('--number',
        help = 'Number of exercise groups (will be extended with numerical IDs)')            
args = parser.parse_args()

further_arg_checking()

send_request_to_gitlab()

# Determine action

#resp = requests.get('https://gitlab.lrz.de/api/v3/projects', headers={'PRIVATE-TOKEN':args.token})
#for project in resp.json():
#    print('{} {}' . format(project['name'], project['owner']['name']))
