import pytest
from utils.generator import read_yml
import os
from FactoryData.ContactForCorpFac import get_subject
import allure

# 存放公共使用的函数

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")

yml_data = read_yml(os.path.join(finance_path, "finance_assistAccoun.yml"))
yml_data1 = read_yml(os.path.join(finance_path, "finance_voucher.yml"))
yml_data2 = read_yml(os.path.join(finance_path, "finance_initbalance.yml"))
yml_data3 = read_yml(os.path.join(finance_path, "finance_asset.yml"))
common = read_yml(os.path.join(finance_path, "common.yml"))


@pytest.fixture(params=yml_data['addContacts']['requestList'])
def get_add_contacts_data(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    # request.param['pkAccountBook'] = yml_data['findContacts']['requestList'][0]['pkAccountBook']
    request.param['contactsCrop'] = get_subject()[0]['subjectName']
    yield request.param
    # 数据清理 删除新增的客户
    # sql = yml_data['addContacts']['sql']
    # delCon = sql['delCon'].format(pkAccountBook=request.param['pkAccountBook'],
    #                               contactsCrop=request.param['contactsCrop'])
    # Del(delCon)


# 查询辅助核算列表
@pytest.fixture(params=yml_data['findContacts']['requestList'])
def get_find_all_contacts_data(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    yield request.param


# 查询科目
@pytest.fixture(params=yml_data1['findInit6']['requestList'])
def get_find_init6_data(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    return request.param


# 查询科目
@pytest.fixture(params=yml_data1['findAllInit']['requestList'])
def get_find_all_init_data(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    return request.param


@pytest.fixture(params=yml_data1['searchVoucher']['requestList'])
def get_find_voucher(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    # request.param['pkAccountBook'] = yml_data1['findInit6']['requestList'][0]['pkAccountBook']
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
    expect_result = get_find_init6_data.pop("expect_result")
    with allure.step("调用查询接口"):
        response = api_http(method, url, headers, get_find_init6_data)
    with allure.step("断言接口响应成功"):
        global allInit6List
        allInit6List = my_assert(response, expect_result)['data']
    get_find_init6_data['expect_result'] = expect_result
    return allInit6List


@pytest.fixture
def get_all_subject_new():
    def _inner(get_find_init6_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data1['findInit6']['content_type'])
        url = get_url(yml_data1['findInit6']['path'])
        method = yml_data1['findInit6']['http_method']
        expect_result = get_find_init6_data.pop("expect_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_init6_data)
        with allure.step("断言接口响应成功"):
            global allInit6List
            allInit6List = my_assert(response, expect_result)['data']
        get_find_init6_data['expect_result'] = expect_result
        return allInit6List

    return _inner


@pytest.fixture
@allure.story("查询所有科目")
def test_find_all_init(get_find_all_init_data, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data1['findAllInit']['content_type'])
    url = get_url(yml_data1['findAllInit']['path'])
    method = yml_data1['findAllInit']['http_method']
    expect_result = get_find_all_init_data.pop("expect_result")
    with allure.step("调用查询接口"):
        response = api_http(method, url, headers, get_find_all_init_data)
    with allure.step("断言接口响应成功"):
        global allInit6List
        allInit6List = my_assert(response, expect_result)['data']
    get_find_all_init_data['expect_result'] = expect_result
    return allInit6List


@allure.story("查询凭证")
@pytest.fixture
def test_find_voucher(get_find_voucher, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data1['searchVoucher']['content_type'])
    url = get_url(yml_data1['searchVoucher']['path'])
    method = yml_data1['searchVoucher']['http_method']
    expect_result = get_find_voucher.pop("expect_result")
    with allure.step("调用接口"):
        response = api_http(method, url, headers, get_find_voucher)
    with allure.step("断言接口响应成功"):
        voucherList = my_assert(response, expect_result)['data']
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
        expect_result = get_del_voucher.pop("expect_result")
        with allure.step("调用接口"):
            response = api_http(method, url, headers, get_del_voucher)
        with allure.step("断言接口响应成功"):
            my_assert(response, expect_result)
        get_del_voucher['expect_result'] = expect_result

    return _inner


@pytest.fixture(params=yml_data2['resetInitial']['requestList'])
def get_reset_init_balance_data(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    # request.param['pkAccountBook'] = yml_data1['findInit6']['requestList'][0]['pkAccountBook']
    return request.param


@allure.story("清空科目及期初余额")
@pytest.fixture
def reset_init_balance():
    def _inner(get_reset_init_balance_data, get_headers, get_url, api_http, get_all_subject_new, my_assert,
               get_find_init6_data):
        headers = get_headers(type=yml_data2['resetInitial']['content_type'])
        url = get_url(yml_data2['resetInitial']['path'])
        method = yml_data2['resetInitial']['http_method']
        with allure.step("调用清空余额接口"):
            # 清空接口
            api_http(method, url, headers, get_reset_init_balance_data)
        with allure.step("调用查询接口校验余额是否清零"):
            # 清空余额后需要重新调用科目列表接口进行校验，不能使用清空之前的查询结果来验证
            subjectList = get_all_subject_new(get_find_init6_data, get_headers, get_url, api_http, my_assert)
            for initBalance in subjectList:
                # 校验对应数据是否被清空
                try:
                    assert initBalance['totalCredit'] == 0  # 本年累计贷方
                    assert initBalance['totalDebit'] == 0  # 本年累计借方
                    assert initBalance['initialBalance'] == 0  # 期初余额
                    assert initBalance['yearsBalance'] == 0  # 年初余额
                except Exception:
                    print('存在问题的科目PK==', initBalance['pkInitialBalance'])
                    assert 0

    return _inner


@pytest.fixture(params=yml_data2['delete']['requestList'])
def get_delete_subject_data(request, test_find_init6):
    request.param['pkAccountBook'] = common['pkAccountBook']
    # request.param['pkAccountBook'] = yml_data1['findInit6']['requestList'][0]['pkAccountBook']
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
        expect_result = get_delete_subject_data.pop("expect_result")
        with allure.step("调用清空余额接口"):
            response = api_http(method, url, headers, get_delete_subject_data)
        my_assert(response, expect_result)

    return _inner


@pytest.fixture(params=yml_data['delContacts']['requestList'])
def get_del_contacts_data(request, test_find_all_contacts, get_headers, get_url, api_http, my_assert,
                          get_find_all_contacts_data):
    # request.param['pkAccountBook'] = common['pkAccountBook']
    # contactList = test_find_all_contacts(get_find_all_contacts_data, get_headers, get_url, api_http, my_assert)
    # request.param['pkContacts'] = contactList[0]['pkContacts']
    # test_find_all_contacts.pop(0)
    return request.param


@allure.story("删除客户")
@pytest.fixture
def del_contacts():
    def _inner(get_del_contacts_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['delContacts']['content_type'])
        url = get_url(yml_data['delContacts']['path'])
        method = yml_data['delContacts']['http_method']
        expect_result = get_del_contacts_data.pop("expect_result")
        with allure.step("调用del接口"):
            response = api_http(method, url, headers, get_del_contacts_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, expect_result)
        get_del_contacts_data['expect_result'] = expect_result

    return _inner


@allure.story("查询辅助核算列表")
# @pytest.mark.run(order=2)
@pytest.fixture
@allure.severity('blocker')
def test_find_all_contacts():
    def _inner(get_find_all_contacts_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findContacts']['content_type'])
        url = get_url(yml_data['findContacts']['path'])
        method = yml_data['findContacts']['http_method']
        expect_result = get_find_all_contacts_data.pop("expect_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_all_contacts_data)
        get_find_all_contacts_data['expect_result'] = expect_result
        with allure.step("断言接口响应成功"):
            global projectList
            projectList = my_assert(response, expect_result)['data']
            # print("查询辅助核算列表", projectList)
        return projectList

    return _inner


@pytest.fixture(params=yml_data3['findAsset']['requestList'])
def get_find_asset_data(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    # request.param['pkAccountBook'] = yml_data['findAssetCard']['requestList'][0]['pkAccountBook']
    return request.param


@allure.story("查询固定资产")
@pytest.mark.run(order=3)
@pytest.fixture
def test_find_asset(get_find_asset_data, get_headers, get_url, api_http, my_assert):
    headers = get_headers(type=yml_data3['findAsset']['content_type'])
    url = get_url(yml_data3['findAsset']['path'])
    method = yml_data3['findAsset']['http_method']
    expect_result = get_find_asset_data.pop("expect_result")
    with allure.step("调用查询接口"):
        response = api_http(method, url, headers, get_find_asset_data)
    with allure.step("断言接口响应成功"):
        global allAssetList
        allAssetList = my_assert(response, expect_result)['data']
        for allAsset in allAssetList:
            # 校验资产状态
            if allAsset['assetsName'] in ("资产B", "资产A"):
                assert allAsset['status'] == 1
            elif allAsset['assetsName'] == '资产C':
                assert allAsset['status'] == 3
    get_find_asset_data['expect_result'] = expect_result
    return allAssetList


@pytest.fixture(params=yml_data3['delAsset']['requestList'])
def get_del_asset_data(request, test_find_asset):
    for allAsset in test_find_asset:
        request.param['pkAssetsCard'] = allAsset['pkAssetsCard']
        # if allAsset['assetsName'] == '测试':
        #     request.param['pkAssetsCard'] = allAsset['pkAssetsCard']
    return request.param


@allure.story("删除固定资产")
@pytest.fixture
def del_asset():
    def _inner(get_del_asset_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data3['delAsset']['content_type'])
        url = get_url(yml_data3['delAsset']['path'])
        method = yml_data3['delAsset']['http_method']
        expect_result = get_del_asset_data.pop("expect_result")
        # print(get_del_asset_data)
        with allure.step("调用删除接口"):
            response = api_http(method, url, headers, get_del_asset_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, expect_result)

    return _inner


@allure.story("查询无形资产类别")
@pytest.fixture(params=yml_data3['findCategory']['requestList'])
def get_intangibleAssetCategory(request, get_headers, get_url, api_http, my_assert):
    request.param['pkAccountBook'] = common['pkAccountBook']
    headers = get_headers(type=yml_data3['findCategory']['content_type'])
    url = get_url(yml_data3['findCategory']['path'])
    method = yml_data3['findCategory']['http_method']
    expect_result = request.param.pop("expect_result")
    with allure.step("调用接口"):
        response = api_http(method, url, headers, request.param)
    with allure.step("断言接口响应成功"):
        categoryList = my_assert(response, expect_result)['data']
    return categoryList


@pytest.fixture(params=yml_data3['delIntangibleAsset']['requestList'])
def get_del_intangible_asset_data(request):
    return request.param


@allure.story("删除无形资产")
@pytest.fixture
def del_IntangibleAsset():
    def _inner(get_del_intangible_asset_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data3['delIntangibleAsset']['content_type'])
        url = get_url(yml_data3['delIntangibleAsset']['path'])
        method = yml_data3['delIntangibleAsset']['http_method']
        expect_result = get_del_intangible_asset_data.pop("expect_result")
        # print(get_del_asset_data)
        with allure.step("调用删除接口"):
            response = api_http(method, url, headers, get_del_intangible_asset_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, expect_result)

    return _inner


@pytest.fixture(params=yml_data3['fuzzySearch']['requestList'])
def get_intangible_asset_data(request):
    request.param['pkAccountBook'] = common['pkAccountBook']
    return request.param


@allure.story("查询无形资产")
@pytest.fixture
def get_all_IntangibleAsset():
    def _inner(get_intangible_asset_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data3['fuzzySearch']['content_type'])
        url = get_url(yml_data3['fuzzySearch']['path'])
        method = yml_data3['fuzzySearch']['http_method']
        expect_result = get_intangible_asset_data.pop("expect_result")
        # print(get_del_asset_data)
        with allure.step("调用接口"):
            response = api_http(method, url, headers, get_intangible_asset_data)
        get_intangible_asset_data['expect_result'] = expect_result
        with allure.step("断言接口响应成功"):
            intangibleList = my_assert(response, expect_result)['data']
        return intangibleList
    return _inner
