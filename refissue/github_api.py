# -*- coding: utf-8 -*-

import httplib2


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
