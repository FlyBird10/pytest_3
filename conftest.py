import requests
import pytest
from utils.readConfig import getBasic


@pytest.fixture()
def get_url():
    root_url, account = getBasic()

    def _inner(path):
        url = root_url + path
        return url, account

    return _inner


@pytest.fixture()
def api_http():
    def _inner(method, url, headers, data=None):
        response = None
        if method == 'post':
            response = requests.post(url, headers=headers, data=data)
        elif method == 'get':
            response = requests.get(url, headers=headers, data=data)
        return response
    return _inner
