import pytest
import requests


@pytest.fixture()
def get_headers_h5(get_Token_h5):
    headers = {}

    def _inner(isGroup=False, type=None):
        # isGroup 是否是群组id   type请求类型
        token = get_Token_h5(isGroup=isGroup)['token']
        if token:
            headers['Authorization'] = 'bearer {0}'.format(token)
        if type == 'form':
            headers['content-type'] = "application/x-www-form-urlencoded"
        elif type == 'json':
            headers['content-type'] = "application/json;charset=UTF-8"
        return headers

    return _inner


@pytest.fixture(scope='session')
def get_Token_h5(get_env):
    '''
    h5登录后获取token
    :param account: need dict {username:,password:}
    :return:token: string
    '''

    # print('this is token function')
    def _inner(account=None, isGroup=False):
        info = {}
        if account is None and isGroup is False:
            # 非群组账户
            account = get_env['account_h5']
        elif isGroup is True:
            # 获取群组账户登录
            account = get_env['account_group']
        else:
            account = account
        root_url = get_env['root_url_h5']
        url = root_url + '/sys/h5/checkBindPhone'
        # print(url)
        data = {"url": url,
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "data": account}
        try:
            r = requests.post(data['url'], data=data['data'], headers=data['headers'])
            if r.json()['data'] is not None:
                info['token'] = r.json()['data']['tokenInfo']['access_token']
                info['pkUser'] = r.json()['data']['userInfo']['pkUser']
                info['pkManagerCorp'] = account['pkManagerCorp']
            else:
                print(r.json())
                print(r.request.headers)
                print(data)
        except Exception as e:
            print(e)
            info['token'] = None
        return info

    return _inner


def test_token(get_Token_h5):
    token = get_Token_h5()
    token_group = get_Token_h5(isGroup=True)
    print('token:===', token)
    print('token_group:===', token_group)
