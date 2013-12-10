# -*- coding: utf-8 -*-

import os
import sys
import webapp2
import logging
import json
import hmac
import sha

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from google.appengine.ext import deferred
import settings

from refissue.models import Issue
from refissue.auth import get_token
from refissue.github_api import request_to_github


class HookHandler(webapp2.RequestHandler):
    def post(self):
        if self._validate_request():
            logging.info('Request from GitHub ----------------------------------')
            event = self.request.headers.get('X-Github-Event')
            content = json.loads(self.request.body)
            deferred.defer(_receive_hook_event, event, content, _queue='hook-event-processing')

    def _validate_request(self):
        return self._is_request_from_github()

    def _is_request_from_github(self):
        signature = self.request.headers.get('X-Hub-Signature')
        token = get_token()
        hashed = hmac.new(token, self.request.body, sha)
        digest = hashed.hexdigest()
        if 'sha1=' + digest == signature:
            return True
        else:
            return False


def _receive_hook_event(event, content):
    if event == 'issues':
        _receive_issue_event(content)


def _receive_issue_event(content):
    if content.get('action') != 'opened':
        logging.info('Receive issue event: action => %s' % content.get('action'))
        return

    opened_issue = Issue.from_dict(content.get('issue'))
    owner = content['repository']['owner']['login']
    repository = content['repository']['name']
    old_issues = Issue.fetch_issues(owner, repository)

    results = opened_issue.search_most_similar_issues(
        old_issues,
        settings.MAX_RESULTS
        )
    candidates = []
    for (similarity, issue) in results:
        if similarity >= settings.SIMILARITY_THRESHOLD:
            candidates.append((similarity, issue))
    if len(candidates) > 0:
        comment = '*How about these issues?* by Refissue.\n'
        for (similarity, issue) in candidates:
            comment += '> #%d (%d%%) "%s"\n' % (issue.number, similarity * 100, issue.title)
        _post_comment_to_issue(owner, repository, opened_issue.number, comment)
    else:
        logging.info('No similar issues found...')

    opened_issue.save(owner, repository)


def _post_comment_to_issue(owner, repo, issue_number, comment):
    body = {
        'body': comment
    }
    token = get_token()
    resp, content = request_to_github(
        token,
        'POST',
        'https://api.github.com/repos/%s/%s/issues/%s/comments' % (owner, repo, issue_number),
        json.dumps(body)
        )
    if int(resp.get('status')) == 201:
        logging.info("""
        --------- Post new comment to issue #%d
        %s
        ---------------------------------------
        """ % (issue_number, comment))
    else:
        logging.error("""
        --------- Failed to post a comment to issue #%d
        %s
        %s
        ---------------------------------------
        """ % (issue_number, resp, content))


application = webapp2.WSGIApplication([
    ('/', HookHandler),
], debug=True)
