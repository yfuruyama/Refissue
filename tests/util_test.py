# -*- coding: utf-8 -*-

import pytest

from refissue.util import save_by, fetch_by


class _MyStore(object):
    def __init__(self, store=None):
        if store is None:
            self.store = {}
        else:
            self.store = store

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value):
        self.store[key] = value

    def __contains__(self, value):
        return value in self.store


_fixtures_save_by = [
    (_MyStore(), 'bar', 'baz')
]

_fixtures_fetch_by = [
    (_MyStore({'foo': 'bar'}), 'foo', 'bar'),
]


class TestUtil(object):
    @pytest.mark.parametrize(('store', 'key', 'value'), _fixtures_save_by)
    def test_save_by(self, store, key, value):
        save_by(key, value, store=store)
        assert key in store

    @pytest.mark.parametrize(('store', 'key', 'value'), _fixtures_save_by)
    def test_fetch_by(self, store, key, value):
        result = fetch_by(key, store=store)
        assert result == value
