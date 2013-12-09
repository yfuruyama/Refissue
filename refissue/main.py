# -*- coding: utf-8 -*-

import os
import sys
import webapp2
import logging
import base64
import json
import hmac
import sha

sys.path.insert(0, 'eggs/httplib2-0.8-py2.7.egg')
sys.path.insert(0, 'eggs/igo_python-0.9.3-py2.7.egg')
import httplib2
from igo.Tagger import Tagger
from models import Issue
from google.appengine.api import memcache
import settings



class HookHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('hi')

    def post(self):
        if validate_request(self.request):
            logging.info('Request from GitHub ----------------------------------')
            event = self.request.headers.get('X-Github-Event')
            content = json.loads(self.request.body)
            receive_hook_event(event, content)


def get_auth_token():
    key = '__token__'
    token = memcache.get(key)
    if token is None:
        credential_file = 'token.json'
        credential = json.load(open(credential_file))
        token = credential.get('token')
        memcache.set(key, token, time=3600)
    return token


def validate_request(request):
    return is_request_from_github(request)


def is_request_from_github(request):
    signature = request.headers.get('X-Hub-Signature')
    token = get_auth_token()
    hashed = hmac.new(token, request.body, sha)
    digest = hashed.digest().encode('hex')
    if 'sha1=' + digest == signature:
        return True
    else:
        return False


def request_to_github(token, method, url, body=None):
    http = httplib2.Http()
    resp, content = http.request(
        url,
        method,
        body=body,
        headers={
            'Authorization': 'token ' + token
        })
    return (resp, content)


def receive_hook_event(event, content):
    if event == 'issues':
        receive_issue_event(content)


def receive_issue_event(content):
    if content.get('action') == 'opened':
        created_issue = Issue.from_dict(content.get('issue'))
        owner = content['repository']['owner']['login']
        repository = content['repository']['name']

        old_issues = fetch_issues(owner, repository)

        logging.info('created #%d: %s' % (created_issue.number, created_issue.body))
        comment = '*How about these issues?*\n'
        for (similarity, issue) in created_issue.search_most_similar_issues(old_issues, settings.MAX_RESULTS):
            if similarity < settings.THRESHOLD:
                continue
            comment += '> #%d (%d%%): "%s"\n' % (issue.number, similarity * 100, issue.title)
            logging.info('#%d(%d%%): %s' % (issue.number, similarity * 100, issue.body))

        body = {
            'body': comment
        }
        token = get_auth_token()
        resp, content = request_to_github(
            token,
            'POST',
            'https://api.github.com/repos/%s/%s/issues/%s/comments' % (owner, repository, created_issue.number),
            json.dumps(body)
            )

    append_issue(created_issue, old_issues)
    memcache_key = '%s:%s' % (owner, repository)
    memcache.set(memcache_key, old_issues, time=3600)

def append_issue(new_one, issues):
    issues = [issue for issue in issues if issue.id != new_one.id]
    issues.append(new_one)
    return issues

def fetch_issues(owner, repo, ignore_cache=False):
    memcache_key = '%s:%s' % (owner, repo)
    issues = memcache.get(memcache_key)
    if issues is None or ignore_cache:
        token = get_auth_token()
        resp, content = request_to_github(
            token,
            'GET',
            'https://api.github.com/repos/%s/%s/issues' % (owner, repo),
            )
        issues = [Issue.from_dict(issue) for issue in json.loads(content)] 
        memcache.set(memcache_key, issues, time=3600)
    return issues


application = webapp2.WSGIApplication([
    ('/', HookHandler),
], debug=True)
