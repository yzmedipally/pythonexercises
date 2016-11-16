#!/bin/sh 

URL='http://localhost'
echo "Fetching TOKEN"
LOGIN='root'
PASSWORD='anatamanarAI'
TOKEN_JSON=$(curl ${URL}/api/v3/session -X POST --data "login=$LOGIN&password=$PASSWORD")
echo "Token fetched:"
echo $TOKEN_JSON
TOKEN=$(echo "${TOKEN_JSON}" | python -c 'import sys, json; print(json.load(sys.stdin)["private_token"])')
echo $TOKEN > .TOKEN

cat > tests/test_config1.json << TESTJSON1
{
    "url": "$URL",
    "pattern": "exercises",
    "downloadDir": "/tmp/exercises_test/",
    "adminMails": [
        "admin.test@tum.de"
    ],
    "students": {
        "1": [
            "john.test@tum.de",
            "peter.test@tum.de"
        ],
        "2": [
            "thomas.test@tum.de"
        ]
    }
}
TESTJSON1

cat > tests/test_config2.json << TESTJSON2
{
    "url": "$URL",
    "pattern": "exercises",
    "downloadDir": "/tmp/exercises_test/",
    "masterGroup": "test-master-group",
    "adminMails": [
        "admin.test@tum.de"
    ],
    "students": {
        "1": [
            "john.test@tum.de",
            "peter.test@tum.de"
        ],
        "2": [
            "thomas.test@tum.de"
        ]
    }
}
TESTJSON2

cat > tests/test_config3.json << TESTJSON3
{
    "url": "$URL",
    "pattern": "exercises",
    "downloadDir": "/tmp/exercises_test/",
    "masterGroup": "test-master-group",
    "adminMails": [
        "admin.test@tum.de"
    ],
    "students": {
        "1": [
            "john.test@tum.de",
            "peter.test@tum.de"
        ],
        "2": [
            "thomas.test@tum.de",
            "latestudent1.test@tum.de"
        ],
        "3": [
        	"latestudent3.test@tum.de"
        ]
    }
}
TESTJSON3

echo "Test-Configs set up:"
ls -l tests/*.json
