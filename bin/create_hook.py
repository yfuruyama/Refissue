#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
import urllib2
import re


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

    option = parser.parse_args()
    has_error, err = _validate_option(option)
    if has_error:
        sys.exit('Failure! ' + err)
    else:
        return option


def _validate_option(option):
    has_error = False
    err = 'No error'
    if re.match(r'^.*/.*$', option.user):
        has_error = True
        err = '-u[--user] option must NOT have \'/\''
    elif re.match(r'^.*/.*$', option.repository):
        has_error = True
        err = '-r[--repository] option must NOT have \'/\''
    return has_error, err


def _create_hook(token, user, repository, hook_endpoint):
    request_body = {
        'name': 'web',
        'active': True,
        'events': [
            'issues'
        ],
        'config': {
            'url': hook_endpoint,
            'content_type': 'json',
            'secret': token  # use token for sha1-secret-key
        },
    }
    print "Now accessing to GitHub..."

    req = urllib2.Request(
        'https://api.github.com/repos/%s/%s/hooks' % (user, repository),
        json.dumps(request_body)
        )
    req.add_header('Authorization', 'token ' + token)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        resp = e
    return (resp.code, resp.read())


def main():
    args = _parse_option()
    credential = json.load(args.credential)
    token = credential.get('token')
    if token is None:
        err = 'No token attribute was found in \'%s\'' % args.credential.name
        sys.exit(err)

    status, content = _create_hook(
        token, args.user, args.repository, args.endpoint
        )

    if status == 201:
        from textwrap import dedent
        success = """
            Success! GitHub Web-hook was created!
            user: {user}
            repository: {repository}
            endpoint: {endpoint}""".format(user=args.user,
                                           repository=args.repository,
                                           endpoint=args.endpoint
                                           )
        print(dedent(success))
        sys.exit(0)
    elif status == 422:
        err = 'Failure! GitHub Web-hook has already been created.'
        sys.exit(err)
    elif status == 404:
        err = 'Failure! Repository \'%s/%s\' not found.' \
            % (args.user, args.repository)
        sys.exit(err)
    else:
        print(content)
        sys.exit('Unexpected Failure!')


if __name__ == '__main__':
    main()
