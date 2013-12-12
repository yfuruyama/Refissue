# -*- coding: utf-8 -*-

import os
import re


def _is_gae_runtime():
    """Whether this runtime is Google App Engine"""
    server_software = os.environ.get('SERVER_SOFTWARE')
    if server_software is not None:
        num = r'\d+'
        gae = r'Google App Engine/%s\.%s\.%s' % (num, num, num)
        gae_dev = r'Development/%s\.%s' % (num, num)
        return bool(re.match(gae, server_software) or
                    re.match(gae_dev, server_software))
    else:
        return False


# in memory default store
_default_store = {}


def save_by(key, value, store=None, **kwargs):
    u""" save data to the persistent or temporary store

    'store' must have both getter and setter, called 'get' and 'set'.
    """
    if store is not None:
        store.set(key, value, **kwargs)
    elif _is_gae_runtime():
        from google.appengine.api import memcache
        memcache.set(key, value, **kwargs)
    else:
        _default_store[key] = value


def fetch_by(key, store=None):
    u""" retrieve data from store
    """
    if store is not None:
        return store.get(key)
    elif _is_gae_runtime():
        from google.appengine.api import memcache
        return memcache.get(key)
    else:
        return _default_store.get(key)
