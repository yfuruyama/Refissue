# -*- coding: utf-8 -*-

import os
import logging
import json

from google.appengine.api import memcache


def get_token():
    key = '__token__'
    token = memcache.get(key)
    if token is None:
        credential_path = os.path.join(
                os.path.dirname(__file__), '..', 'token.json'
                )
        credential = json.load(open(credential_path))
        token = str(credential.get('token')) # need converting to str
        memcache.set(key, token, time=3600)
    return str(token)
