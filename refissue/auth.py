# -*- coding: utf-8 -*-

import os
import json

import settings
from refissue.util import save_by, fetch_by


def get_token():
    temporary_store_key = '{owner}:{repo}'
    temporary_store_expire = 3600

    token = fetch_by(temporary_store_key)
    if token is None:
        credential_path = os.path.join(
            os.path.dirname(__file__), '..', settings.CREDENTIAL_PATH
            )
        credential = json.load(open(credential_path))
        token = str(credential.get('token'))  # need converting to str
        save_by(temporary_store_key, token, time=temporary_store_expire)
    return str(token)
