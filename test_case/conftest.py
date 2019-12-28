import pytest
import requests
from utils.readConfig import *


@pytest.fixture()
def get_Token(account=None):
    '''

    :param account: need dict {username:,password:}
    :return:
    '''
    url = get_url()
    if account is None:
        account = get_account()
    else:
        account = account
    url = url + '/sys/login'
    data = {"url": url,
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": account}
    try:
        r = requests.post(data['url'], data=data['data'], headers=data['headers'])
        assert r.status_code == 200
        token = r.json()['access_token']
    except Exception as e:
        print(e)
        token = None
    return token


def test_corp(get_Token):
    url = get_url()
    url = url + '/platform/loginResult'
    data = {"url": url,
            "headers": {
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": 'bearer {0}'.format(get_Token)
            }}
    r = requests.post(url=data['url'], headers=data['headers'])
    # print(r.json())
    # assert r.status_code == 200
    # print(r.status_code)
    corpList = r.json()['data']['userInfo']['dzCorp']
    # pkCorpList = []
    # for item in corpList:
    #     pkCorpList.append(item['pkCorp'])
    pkCorpList = [item['pkCorp'] for item in corpList]
    pkCorp = pkCorpList[-1]
    print(pkCorpList)
    return pkCorp


@pytest.fixture()
def get_headers(get_Token):
    def _inner(type=None):
        headers = {}
        headers['Authorization'] = 'bearer {0}'.format(get_Token)
        if get_Token:
            headers['pkmanagercorp'] = test_corp(get_Token)
        if type == 'form':
            headers['content-type'] = "application/x-www-form-urlencoded"
        elif type == 'json':
            headers['content-type'] = "application/json;charset=UTF-8"
        print(headers)
        return headers

    return _inner
