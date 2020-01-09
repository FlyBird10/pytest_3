import requests
import pytest
from utils.readConfig import get_root_url, get_account, get_mysql
import pymysql
import os


@pytest.fixture()
def get_url(get_env):
    root_url = get_env['root_url']

    def _inner(path):
        url = root_url + path
        return url

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


def pytest_addoption(parser):
    group = parser.getgroup('yun_known')
    group.addoption('--env',
                    default='test',
                    help='choose run case env:test/pro')


@pytest.fixture(scope='session')
def get_env(request):
    env = request.config.getoption('env')
    info = {}
    if env == 'test':
        info['root_url'] = get_root_url(env='test')
        info['account'] = get_account(env='test')
        info['mysql'] = get_mysql(env='test')
    elif env == 'pro':
        info['root_url'] = get_root_url(env='pro')
        info['account'] = get_account(env='pro')
        info['mysql'] = get_mysql(env='pro')

    return info


@pytest.fixture(scope='session')
def get_Token(get_env, account=None):
    '''

    :param account: need dict {username:,password:}
    :return:
    '''
    print('this is token function')
    if account is None:
        account = get_env['account']
    else:
        account = account
    root_url = get_env['root_url']
    url = root_url + '/sys/login'
    # print(url)
    data = {"url": url,
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": account}
    try:
        r = requests.post(data['url'], data=data['data'], headers=data['headers'])
        token = r.json()['access_token']
    except Exception as e:
        print(e)
        token = None
    return token, root_url


def test_corp(get_Token):
    token, root_url = get_Token
    url = root_url + '/platform/loginResult'
    data = {"url": url,
            "headers": {
                "content-type": "application/x-www-form-urlencoded",
                "Authorization": 'bearer {0}'.format(token)
            }}
    r = requests.post(url=data['url'], headers=data['headers'])
    corpList = r.json()['data']['userInfo']['dzCorp']
    pkCorpList = [item['pkCorp'] for item in corpList]
    pkCorp = pkCorpList[0]
    print(pkCorpList)
    return pkCorp


@pytest.fixture()
def get_headers(get_Token):
    def _inner(type=None):
        headers = {}
        headers['Authorization'] = 'bearer {0}'.format(get_Token[0])
        if get_Token:
            headers['pkmanagercorp'] = test_corp(get_Token)
        if type == 'form':
            headers['content-type'] = "application/x-www-form-urlencoded"
        elif type == 'json':
            headers['content-type'] = "application/json;charset=UTF-8"
        # print(headers)
        return headers

    return _inner


@pytest.fixture(scope="session")
def mysql(get_env):
    mysql = get_env['mysql']
    con = pymysql.connect(mysql['host'], mysql['account'], mysql['pwd'], mysql['dbname'])  # 链接MySQL
    print('=========create mysql connection========')
    cursor = con.cursor()  # 获取操作游标
    yield cursor  # 等同于return
    print('==========close mysql connection====')
    con.close()  # 关闭链接


@pytest.fixture()
def execute_sql(mysql):
    def _inner(sql):
        mysql.execute(sql)
        result = mysql.fetchall()
        return result

    return _inner


@pytest.fixture(scope="session")
def get_path():
    path = {}
    path['root_path'] = os.path.dirname(__file__)
    path['data_path'] = os.path.join(path['root_path'], "data")
    path['test_path'] = os.path.join(path['root_path'], "test_case")
    path['template_file'] = os.path.join(path['test_path'], 'template_api')
    return path


def test_token(get_path):
    # print(execute_sql("select *From tbl_sycs_user limit 1"))
    # print(execute_sql("select *From tbl_sycs_user limit 1"))
    print(get_path)
