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


@pytest.fixture(params=yml_data['addContacts']['requestList'])
def get_add_contacts_data(request):
    request.param['pkAccountBook'] = yml_data['findContacts']['requestList'][0]['pkAccountBook']
    request.param['contactsCrop'] = get_subject()[0]['subjectName']
    yield request.param
    # 数据清理 删除新增的客户
    sql = yml_data['addContacts']['sql']
    delCon = sql['delCon'].format(pkAccountBook=request.param['pkAccountBook'],
                                  contactsCrop=request.param['contactsCrop'])
    Del(delCon)


# 查询辅助核算列表
@pytest.fixture(params=yml_data['findContacts']['requestList'])
def get_find_all_contacts_data(request):
    return request.param


# 查询科目
@pytest.fixture(params=yml_data1['findInit6']['requestList'])
def get_find_init6_data(request):
    return request.param


@allure.story("查询科目")
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





# @pytest.fixture()
# def dealData(get_find_voucher, get_del_voucher, get_headers, get_url, api_http, my_assert):
#     print("执行dealData fixture")
#     # 清理测试过程中产生的数据
#     pkVouchers = TestVoucher().test_find_voucher(get_find_voucher, get_headers, get_url, api_http, my_assert)
#     for pkVoucher in pkVouchers:
#         get_del_voucher['pkVoucher'] = pkVoucher  # 更新凭证主键
#         print("pkVoucher: ", pkVoucher)
#         TestVoucher().del_voucher(get_del_voucher, get_headers, get_url, api_http, my_assert)
