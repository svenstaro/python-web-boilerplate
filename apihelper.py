#!/usr/bin/env python
"""API Helper to ease making API calls to this Python API.

It does things such as fetching a token for every request with username and
password.
"""

import argparse
import json
from urllib.parse import urlparse, parse_qs
import requests
from pprint import pprint

DEFAULT_USERNAME = 'test@example.com'
DEFAULT_PASSWORD = 'test'


def _parse_args():
    """Parse command line arguments."""
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


def _acquire_token(url, username, password):
    """Login with `username` and `password` and return the resulting token."""
    token = None
    # First get a token
    data = {
        'email': username,
        'password': password,
    }
    resp = requests.post("{host}/login".format(host=host), json=data)

    if resp.status_code != 200:
        print("ERROR")  # noqa: T003
        try:
            pprint(resp.json())
        except ValueError:
            print(resp)  # noqa: T003
        finally:
            exit(1)

    token = resp.json()['data']
    return token


def _do_request(args, token):
    """Do the actual request to with the attributes set in `args` using `token`."""
    headers = {
        'Accept': 'application/json',
        'user-agent': 'API Helper 1.0',
        'Authorization': 'Bearer {token}'.format(token=token),
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
        print("No valid method provided.")  # noqa: T003
        exit(1)


if __name__ == "__main__":
    args = _parse_args()

    parsed_url = urlparse(args.url)
    host = "{scheme}://{netloc}".format(scheme=parsed_url.scheme, netloc=parsed_url.netloc)
    login_url = "{host}/login".format(host=host)
    token = _acquire_token(login_url, args.username, args.password)

    resp = _do_request(args, token)

    if args.parseable:
        print(json.dumps(resp.json()))  # noqa: T003
    else:
        pprint(resp.json())
