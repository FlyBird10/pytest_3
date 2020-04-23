import requests
import pytest
from utils.readConfig import get_root_url, get_account, get_mysql, get_redis
import pymysql
import os
import allure
import json
# from test_case.test_finance.test_O3_voucher import TestVoucher
# from test_case.test_finance.test_O3_voucher import TestVoucher


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
        content = headers['content-type']
        # print(content)
        if 'json' in content:
            data = json.dumps(data)  # headers为json格式时，参数也必须转为json
        if method == 'post':
            response = requests.post(url, headers=headers, data=data)
        elif method == 'get':
            # get请求参数必须使用params传递
            response = requests.get(url, headers=headers, params=data)
        elif method == 'delete':
            response = requests.delete(url, headers=headers, data=data)
        return response

    return _inner


def pytest_addoption(parser):
    group = parser.getgroup('yun_known')
    group.addoption('--env',
                    default='test',
                    help='choose run case env:test/pro')


@pytest.fixture(scope='session')
def get_env(request):
    # 划分测试环境
    env = request.config.getoption('env')
    info = {}
    if env == 'test':
        # 测试环境账户
        info['root_url'] = get_root_url(env='test')
        info['account'] = get_account(env='test')
        info['mysql'] = get_mysql(env='test')
        info['root_url_h5'] = get_root_url(env='h5_test')
        info['redis'] = get_redis(env='test')
        info['account_h5'] = get_account(env='h5_test')
        info['account_group'] = get_account(env='group_account')
    elif env == 'pro':
        # 线上环境账户
        info['root_url'] = get_root_url(env='pro')
        info['account'] = get_account(env='pro')
        info['mysql'] = get_mysql(env='pro')
        info['root_url_h5'] = get_root_url(env='h5_pro')
        info['account_h5'] = get_account(env='h5_pro')
        info['account_group'] = get_account(env='group_account_pro')
    return info


@pytest.fixture(scope='session')
def get_Token(get_env, account=None):
    '''
    登录后获取token
    :param account: need dict {username:,password:}
    :return:
    '''
    # print('this is token function')
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
    '''
    获取用户所在的代账公司
    :param get_Token:
    :return:
    '''
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
    # print(pkCorpList)
    return pkCorp


@pytest.fixture()
def get_headers(get_Token):
    def _inner(type='form', content=None):
        headers = {}
        headers['Authorization'] = 'bearer {0}'.format(get_Token[0])
        if get_Token:
            headers['pkmanagercorp'] = test_corp(get_Token)
        if type == 'form':
            headers['content-type'] = "application/x-www-form-urlencoded"
        elif type == 'json':
            headers['content-type'] = "application/json;charset=UTF-8"
        elif type == 'multipart':
            headers['content-type'] = content
        # print(headers)
        return headers

    return _inner


@pytest.fixture()
def get_headers_Notoken():
    # 无token的headers
    def _inner(type=None):
        headers = {}
        if type == 'form':
            headers['content-type'] = "application/x-www-form-urlencoded"
        elif type == 'json':
            headers['content-type'] = "application/json;charset=UTF-8"
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


@pytest.fixture()
@allure.step('校验接口响应代码和提示语')
def my_assert():
    def _inner(response, except_result):
        if response.status_code == 200:
            response_json = response.json()
            try:
                assert int(response_json['code']) == int(except_result['code'])
                assert response_json['message'] == except_result['message']
            except Exception:
                print("实际结果：", response_json)
                print("期望结果：", except_result)
                print(response.request.url)
                print(response.request.body)
                print(response.request.headers)
                assert 0
            return response_json
        else:
            print(response.request.url)
            print(response.request.body)
            print(response.request.headers)
            print(response.content)
            assert 0

    return _inner


def test_token(get_path, api_http, get_headers_h5):
    # print(execute_sql("select *From tbl_sycs_user limit 1"))
    # print(execute_sql("select *From tbl_sycs_user limit 1"))
    # print(get_path)
    headers = {
        "Authorization": "Bearer 4512b1d9-3680-4ffd-8bc6-42375eb9d767"
    }
    data = {
        "pkQuestion": "045a2e8fe4384f8e9470032dc47585f7",
        "controlType": "del"
    }
    # res = api_http("get", "http://192.168.2.253:9998/knowledge/question/validStatus", headers, data=data)
    # print(res.json())
    # print(res.request.url)
    # print(res.request.method)
    print(get_headers_h5(type='json'))
    # print(get_Token_h5)


def pytest_configure(config):
    # 运行报错PytestUnknownMarkWarning 故添加以下代码
    marker_list = ["run", "skip", "dependency"]  # 标签名集合
    for markers in marker_list:
        config.addinivalue_line(
            "markers", markers
        )


# @pytest.fixture(scope='session')
# def dealData(get_find_voucher, get_del_voucher):
#     print("执行dealData fixture")
#     # 清理测试过程中产生的数据
#     pkVouchers = TestVoucher().test_find_voucher(get_find_voucher, get_headers, get_url, api_http, my_assert)
#     for pkVoucher in pkVouchers:
#         get_del_voucher['pkVoucher'] = pkVoucher  # 更新凭证主键
#         print("pkVoucher: ", pkVoucher)
#         TestVoucher().del_voucher(get_del_voucher, get_headers, get_url, api_http, my_assert)

