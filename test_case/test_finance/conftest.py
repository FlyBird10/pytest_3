import pytest
from utils.generator import read_yml
import os
from FactoryData.ContactForCorpFac import get_subject
import allure
from test_case.test_finance.test_O3_voucher import TestVoucher
from utils.DBUtil import Del

# 存放公共使用的函数

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")

yml_data = read_yml(os.path.join(finance_path, "finance_assistAccoun.yml"))
yml_data1 = read_yml(os.path.join(finance_path, "finance_voucher.yml"))
yml_data2 = read_yml(os.path.join(finance_path, "finance_initbalance.yml"))


# @pytest.fixture(params=yml_data['addContacts']['requestList'])
# def get_add_contacts_data(request):
#     request.param['pkAccountBook'] = yml_data['findContacts']['requestList'][0]['pkAccountBook']
#     request.param['contactsCrop'] = get_subject()[0]['subjectName']
#     yield request.param
#     # 数据清理 删除新增的客户
#     # sql = yml_data['addContacts']['sql']
#     # delCon = sql['delCon'].format(pkAccountBook=request.param['pkAccountBook'],
#     #                               contactsCrop=request.param['contactsCrop'])
#     # Del(delCon)
#
#
# 查询辅助核算列表
@pytest.fixture(params=yml_data['findContacts']['requestList'])
def get_find_all_contacts_data(request):
    return request.param


# 查询科目
@pytest.fixture(params=yml_data1['findInit6']['requestList'])
def get_find_init6_data(request):
    return request.param


# 查询科目
@pytest.fixture(params=yml_data1['findAllInit']['requestList'])
def get_find_all_init_data(request):
    request.param['pkAccountBook'] = yml_data1['findInit6']['requestList'][0]['pkAccountBook']
    return request.param


@pytest.fixture(params=yml_data1['searchVoucher']['requestList'])
def get_find_voucher(request):
    request.param['pkAccountBook'] = yml_data1['findInit6']['requestList'][0]['pkAccountBook']
    yield request.param


@pytest.fixture(params=yml_data1['delVoucher']['requestList'])
def get_del_voucher(request):
    return request.param


@allure.story("查询所有科目")
@pytest.mark.run(order=1)
@allure.severity('blocker')
@pytest.fixture
def test_find_init6(get_find_init6_data, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data1['findInit6']['content_type'])
    url = get_url(yml_data1['findInit6']['path'])
    method = yml_data1['findInit6']['http_method']
    except_result = get_find_init6_data.pop("except_result")
    with allure.step("调用查询接口"):
        response = api_http(method, url, headers, get_find_init6_data)
    with allure.step("断言接口响应成功"):
        global allInit6List
        allInit6List = my_assert(response, except_result)['data']
    get_find_init6_data['except_result'] = except_result
    return allInit6List


@pytest.fixture
@allure.story("查询所有科目")
def test_find_all_init(get_find_all_init_data, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data1['findAllInit']['content_type'])
    url = get_url(yml_data1['findAllInit']['path'])
    method = yml_data1['findAllInit']['http_method']
    except_result = get_find_all_init_data.pop("except_result")
    with allure.step("调用查询接口"):
        response = api_http(method, url, headers, get_find_all_init_data)
    with allure.step("断言接口响应成功"):
        global allInit6List
        allInit6List = my_assert(response, except_result)['data']
    get_find_all_init_data['except_result'] = except_result
    return allInit6List


@allure.story("查询凭证")
@pytest.fixture
def test_find_voucher(get_find_voucher, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data1['searchVoucher']['content_type'])
    url = get_url(yml_data1['searchVoucher']['path'])
    method = yml_data1['searchVoucher']['http_method']
    except_result = get_find_voucher.pop("except_result")
    with allure.step("调用接口"):
        response = api_http(method, url, headers, get_find_voucher)
    with allure.step("断言接口响应成功"):
        voucherList = my_assert(response, except_result)['data']
    global pkVouchers
    pkVouchers = []
    if len(voucherList) > 0:
        for voucher in voucherList:
            pkVouchers.append(voucher['pkVoucher'])
    return pkVouchers


@pytest.fixture(params=yml_data1['delVoucher']['requestList'])
def get_del_voucher(request):
    return request.param


@allure.story("删除凭证")
@pytest.fixture
def del_voucher():
    def _inner(get_del_voucher, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data1['delVoucher']['content_type'])
        url = get_url(yml_data1['delVoucher']['path'])
        method = yml_data1['delVoucher']['http_method']
        except_result = get_del_voucher.pop("except_result")
        with allure.step("调用接口"):
            response = api_http(method, url, headers, get_del_voucher)
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)
        get_del_voucher['except_result'] = except_result

    return _inner


@pytest.fixture(params=yml_data2['resetInitial']['requestList'])
def get_reset_init_balance_data(request):
    request.param['pkAccountBook'] = yml_data1['findInit6']['requestList'][0]['pkAccountBook']
    return request.param


@allure.story("清空科目及期初余额")
@pytest.fixture
def reset_init_balance():
    def _inner(get_reset_init_balance_data, get_headers, get_url, api_http):
        headers = get_headers(type=yml_data2['resetInitial']['content_type'])
        url = get_url(yml_data2['resetInitial']['path'])
        method = yml_data2['resetInitial']['http_method']
        with allure.step("调用清空余额接口"):
            # 清空接口
            api_http(method, url, headers, get_reset_init_balance_data)
        with allure.step("调用查询接口校验余额是否清零"):
            for initBalance in test_find_init6:
                # 校验对应数据是否被清空
                assert initBalance['totalCredit'] == 0  # 本年累计贷方
                assert initBalance['totalDebit'] == 0  # 本年累计借方
                assert initBalance['initialBalance'] == 0  # 期初余额
                assert initBalance['yearsBalance'] == 0  # 年初余额

    return _inner


@pytest.fixture(params=yml_data2['delete']['requestList'])
def get_delete_subject_data(request, test_find_init6):
    request.param['pkAccountBook'] = yml_data1['findInit6']['requestList'][0]['pkAccountBook']
    for initBalance in test_find_init6:
        # print(initBalance)
        if request.param['pkInitialBalance'] in initBalance['subjectName']:
            print(initBalance['subjectName'])
            request.param['pkInitialBalance'] = initBalance['pkInitialBalance']
            request.param['subjectCode'] = initBalance['subjectCode']
    return request.param


@allure.story("删除科目")
@pytest.fixture
def delete_subject():
    def _inner(get_delete_subject_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data2['delete']['content_type'])
        url = get_url(yml_data2['delete']['path'])
        method = yml_data2['delete']['http_method']
        except_result = get_delete_subject_data.pop("except_result")
        with allure.step("调用清空余额接口"):
            response = api_http(method, url, headers, get_delete_subject_data)
        my_assert(response, except_result)

    return _inner


@pytest.fixture(params=yml_data['delContacts']['requestList'])
def get_del_contacts_data(request, test_find_all_contacts):
    request.param['pkContacts'] = test_find_all_contacts[0]['pkContacts']
    test_find_all_contacts.pop(0)
    return request.param


@allure.story("删除客户")
@pytest.fixture
def del_contacts():
    def _inner(get_del_contacts_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['delContacts']['content_type'])
        url = get_url(yml_data['delContacts']['path'])
        method = yml_data['delContacts']['http_method']
        except_result = get_del_contacts_data.pop("except_result")
        with allure.step("调用del接口"):
            response = api_http(method, url, headers, get_del_contacts_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)

    return _inner


@allure.story("查询辅助核算列表")
@pytest.mark.run(order=2)
@pytest.fixture
@allure.severity('blocker')
def test_find_all_contacts(get_find_all_contacts_data, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data['findContacts']['content_type'])
    url = get_url(yml_data['findContacts']['path'])
    method = yml_data['findContacts']['http_method']
    except_result = get_find_all_contacts_data.pop("except_result")
    with allure.step("调用查询接口"):
        response = api_http(method, url, headers, get_find_all_contacts_data)
    get_find_all_contacts_data['except_result'] = except_result
    with allure.step("断言接口响应成功"):
        global projectList
        projectList = my_assert(response, except_result)['data']
        # print("查询辅助核算列表", projectList)
    return projectList


@pytest.fixture(params=yml_data['findAsset']['requestList'])
def get_find_asset_data(request):
    request.param['pkAccountBook'] = yml_data['findAssetCard']['requestList'][0]['pkAccountBook']
    return request.param


@allure.story("查询固定资产")
@pytest.mark.run(order=3)
@pytest.fixture
def test_find_asset(get_find_asset_data, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data['findAsset']['content_type'])
    url = get_url(yml_data['findAsset']['path'])
    method = yml_data['findAsset']['http_method']
    except_result = get_find_asset_data.pop("except_result")
    with allure.step("调用查询接口"):
        response = api_http(method, url, headers, get_find_asset_data)
    with allure.step("断言接口响应成功"):
        global allAssetList
        allAssetList = my_assert(response, except_result)['data']
        for allAsset in allAssetList:
            # 校验资产状态
            if allAsset['assetsName'] in ("资产B", "资产A"):
                assert allAsset['status'] == 1
            elif allAsset['assetsName'] == '资产C':
                assert allAsset['status'] == 3


@pytest.fixture(params=yml_data['delAsset']['requestList'])
def get_del_asset_data(request):
    for allAsset in allAssetList:
        if allAsset['assetsName'] == '测试':
            request.param['pkAssetsCard'] = allAsset['pkAssetsCard']
    return request.param


@allure.story("删除固定资产")
@pytest.mark.run(order=4)
@pytest.fixture
def test_del_asset(get_del_asset_data, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data['delAsset']['content_type'])
    url = get_url(yml_data['delAsset']['path'])
    method = yml_data['delAsset']['http_method']
    except_result = get_del_asset_data.pop("except_result")
    # print(get_del_asset_data)
    with allure.step("调用删除接口"):
        response = api_http(method, url, headers, get_del_asset_data)
    with allure.step("断言接口响应成功"):
        my_assert(response, except_result)
