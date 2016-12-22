#!/usr/bin/env python

import argparse
import json
from urllib.parse import urlparse, parse_qs
import requests
from pprint import pprint

DEFAULT_USERNAME = 'test@example.com'
DEFAULT_PASSWORD = 'test'


def parse_args():
    parser = argparse.ArgumentParser(description='API convenience helper')
    parser.add_argument('-u', '--username', default=DEFAULT_USERNAME)
    parser.add_argument('-p', '--password', default=DEFAULT_PASSWORD)
    parser.add_argument('-X', '--request', default="GET")
    parser.add_argument('-d', '--data')
    parser.add_argument('-F', '--form')
    parser.add_argument('--parseable', action='store_true', help="Don't pretty print the output")
    parser.add_argument('url', metavar='URL')

    args = parser.parse_args()
    return args


def acquire_token(url, username, password):
    token = None
    # First get a token
    data = {
        'email': username,
        'password': password,
    }
    resp = requests.post("{}/login".format(host), json=data)

    if resp.status_code != 200:
        print("ERROR")
        try:
            pprint(resp.json())
        except ValueError:
            print(resp)
        finally:
            exit(1)

    token = resp.json()['data']
    return token


def do_request(url, token):
    headers = {
        'Accept': 'application/json',
        'user-agent': 'API Helper 1.0',
        'Authorization': 'Bearer {}'.format(token)
    }

    # Now use that token to make the actual API request
    if args.request == "GET":
        resp = requests.get(args.url, headers=headers)
        return resp
    elif args.request == "POST":
        data = None
        form = None

        # Get either payload or form data
        if args.data:
            # Payload data is expected in JSON format
            data = json.loads(args.data)
        elif args.form:
            form = parse_qs(args.form)

        files = {}
        if form:
            form['image'][0] = form['image'][0].replace('@', '')
            files = {'image': (form['filename'][0], open(form['image'][0], 'rb'), form['type'][0])}
        elif data:
            headers['Content-Type'] = 'application/json'
        resp = requests.post(args.url, json=data, files=files, headers=headers)
        return resp
    elif args.request == "DELETE":
        resp = requests.delete(args.url, headers=headers)
        return resp
    else:
        print("No valid method provided.")
        exit(1)


if __name__ == "__main__":
    args = parse_args()

    parsed_url = urlparse(args.url)
    host = "{}://{}".format(parsed_url.scheme, parsed_url.netloc)
    login_url = "{}/login".format(host, auth=(args.username, args.password))
    token = acquire_token(login_url, args.username, args.password)

    resp = do_request(args.url, token)

    if args.parseable:
        print(json.dumps(resp.json()))
    else:
        pprint(resp.json())
