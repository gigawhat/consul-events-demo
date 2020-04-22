#!/usr/bin/python3

import base64
import json
import os
import requests
import sys

HOSTNAME = os.environ['HOSTNAME']

def decode_payload(payload):
    return json.loads(base64.b64decode(payload))


def event_for_me(event):
    payload = decode_payload(event['Payload'])
    return payload['drain'] == HOSTNAME


def put_in_maintenace_mode():
    url = 'http://localhost:8500/v1/agent/maintenance'
    params = {
        'enable': True,
        'reason': "auto scaler event"
    }
    try:
        r = requests.put(url, params=params)
        r.raise_for_status()

    except requests.exceptions.HTTPError as e: 
        print(e)
        sys.exit(1)

def main():
    try:
        event = json.load(sys.stdin)[-1]
    
    except IndexError:
        print("event was not a list. agent must be starting")
        sys.exit(0)

    if event_for_me(event):
        print("event was for me!")
        put_in_maintenace_mode()
    else:
        print("ignoring event")


if __name__ == '__main__':
    main()