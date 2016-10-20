#!/bin/sh

./tests/01_create_configfiles.sh

pecho() { printf %s\\n "$*"; }
log() {
    [ "$#" -eq 0 ] || { pecho "$@"; return 0; }
    while IFS= read -r log_line || [ -n "${log_line}" ]; do
        log "${log_line}"
    done
}
error() { log "ERROR: $@" >&2; }
fatal() { error "$@"; exit 1; }
try() { "$@" || fatal "'$@' failed"; }

GREEN='\033[0;32m'
OK() { printf "${GREEN}OK${NC}\\n"; }

testcase() {
    testname=$1; shift
    testscript=$1; shift
    printf %s "Testing ${testname}... "
    eval "${testscript}" || fatal "test failed"
    OK
    printf ""
}

curl -I http://localhost
curl -I https://localhost

ln -s tests/test_config1.json config.json
testcase "exercises: default help" '
    OUTPUT=$(python exercises.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "Exercises - Script to automate gitlab course handling."
'

testcase "exercises: help" '
    OUTPUT=$(python exercises.py --help 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "Exercises - Script to automate gitlab course handling."
'

mkdir -p /tmp/exercises_test/
testcase "gitlab: prepare users" '
    OUTPUT=$(python 02_create_users.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "exercises: action check" '
    OUTPUT=$(python exercises.py --config test_config1.json --action check 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "KeyError: 'masterGroup'"
'

testcase "gitlab: create master group" '
	OUTPUT=$(python 03_create_group.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "gitlab: create master project" '
	OUTPUT=$(python 04_create_project.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "exercises: action initialize groups" '
    OUTPUT=$(python exercises.py --config test_config2.json --action init 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "Successfully created project with config-file"
'

testcase "gitlab: check initalized groups" '
	OUTPUT=$(python 05_check_init.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "gitlab: add file to master project" '
	OUTPUT=$(python 06_add_file.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "exercises: action publish" '
    OUTPUT=$(python exercises.py --config test_config2.json --action publish --exercise testex1 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "???"
'

testcase "gitlab: check published files" '
	OUTPUT=$(python 07_check_file.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "exercises: action add reviewer" '
    OUTPUT=$(python exercises.py --config test_config2.json --action add_reviewer --exercise testex1 --reviewer reviewer.test@tum.de 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "???"
'

testcase "exercises: action download" '
    OUTPUT=$(python exercises.py --config test_config2.json --action download --exercise testex1 --duedate 'date +%s' 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "???"
'

# ToDo: check for files in /tmp/exercises_test/

testcase "gitlab: prepare " '
	OUTPUT=$(python 08_create_idempotenz.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "exercises: action initialize groups idempotenztest" '
    OUTPUT=$(python exercises.py --config test_config3.json --action init 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "Successfully created project with config-file"
'

testcase "exercises: action publish idempotenztest" '
    OUTPUT=$(python exercises.py --config test_config3.json --action publish --exercise testex1 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "???"
'

testcase "gitlab: check published files idempotenztest" '
	OUTPUT=$(python 09_check_idempotenz.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'

testcase "exercises: action add reviewer idempotenztest" '
    OUTPUT=$(python exercises.py --config test_config3.json --action add_reviewer --exercise testex1 --reviewer reviewer.test@tum.de 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "???"
'

testcase "gitlab: clean up" '
	OUTPUT=$(python 10_cleanup.py 2>&1) || exit 1
    pecho "${OUTPUT}" | grep -q "OK"
'
