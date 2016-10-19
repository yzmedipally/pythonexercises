#!/bin/sh

URL='http://192.168.99.100:8080'

LOGIN='root'
PASSWORD='5iveL!fe'
TOKEN_JSON=$(curl -s ${URL}/api/v3/session -X POST --data "login=$LOGIN&password=$PASSWORD")
TOKEN=$(echo "${TOKEN_JSON}" | python -c 'import sys, json; print(json.load(sys.stdin)["private_token"])')

cat > tests/test_config1.json << TESTJSON1
{
    "url": "$URL",
    "token": "$TOKEN",
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
    "token": "$TOKEN",
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
    "token": "$TOKEN",
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