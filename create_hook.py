#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse

import httplib2


def _parse_option():
    parser = argparse.ArgumentParser(description='Create GitHub Web Hook.')
    parser.add_argument(
        '-u', '--user', required=True, help='GitHub user'
        )
    parser.add_argument(
        '-r', '--repository', required=True, help='GitHub repository'
        )
    parser.add_argument(
        '-e', '--endpoint', required=True, help='Hook endpoint'
        )
    parser.add_argument(
        '-c', '--credential', nargs='?', type=argparse.FileType('r'),
        default='credential.json'
        )
    return parser.parse_args()


def _create_hook(token, user, repository, hook_endpoint):
    http = httplib2.Http()
    request_body = {
        'name': 'web',
        'active': True,
        'events': [
            'issues'
        ],
        'config': {
            'url': hook_endpoint,
            'content_type': 'json',
            'secret': token # use token for sha1-secret-key
        },
    }
    print "Now accessing to GitHub...\n"
    resp, content = http.request(
        'https://api.github.com/repos/%s/%s/hooks' % (user, repository),
        'POST',
        body=json.dumps(request_body),
        headers={
            'Authorization': 'token ' + token
        })
    return (resp, content)


def main():
    args = _parse_option()
    credential = json.load(args.credential)
    token = credential.get('token')
    if token is None:
        err = 'No token attribute was found in \'%s\'' % args.credential.name
        sys.exit(err)

    resp, content = _create_hook(
        token, args.user, args.repository, args.endpoint
        )

    status = resp.get('status')
    if status == '201':
        success = 'Success! GitHub Web-hook was created: endpoint => %s' \
            % args.endpoint
        print(success)
        sys.exit(0)
    elif status == '422':
        err = 'Failure! GitHub Web-hook has already been created.'
        sys.exit(err)
    elif status == '404':
        err = 'Failure! Repository \'%s/%s\' not found.' \
            % (args.user, args.repository)
        sys.exit(err)
    else:
        print(content)
        sys.exit('Unexpected Failure!')


if __name__ == '__main__':
    main()
