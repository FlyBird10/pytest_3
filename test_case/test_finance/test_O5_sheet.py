from utils.generator import read_yml
import pytest
import allure
import os

# from test_case.test_finance.test_O3_voucher import TestVoucher

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_sheet.yml"))


@allure.feature("报表")
class TestSheet:
    @pytest.fixture(params=yml_data['statementAllData']['requestList'])
    def get_find_all_data(self, request):
        request.param['pkAccountBook'] = yml_data['statementAllData']['requestList'][0]['pkAccountBook']
        yield request.param

    @allure.story("查询资产负债表")
    @pytest.mark.run(order=1)
    def test_find_all(self, get_find_all_data, get_headers, get_url, api_http):
        assert_data = get_find_all_data.pop("assert_data")
        headers = get_headers(type=yml_data['statementAllData']['content_type'])
        url = get_url(yml_data['statementAllData']['path'])
        method = yml_data['statementAllData']['http_method']
        with allure.step("调用查询接口"):
            res = api_http(method, url, headers, get_find_all_data).json()
        # print(res)
        sheetList = res['financialStatementsts']
        # print(sheetList)
        for my_assert in assert_data:
            for sheet in sheetList:
                if my_assert['name'] == sheet['name']:
                    # print(my_assert['name'])
                    assert my_assert['finalBalance'] == sheet['finalBalance']
                    assert my_assert['beginBalance'] == sheet['beginBalance']

    @pytest.fixture(params=yml_data['getProfitData']['requestList'])
    def get_ProfitData_data(self, request):
        request.param['pkAccountBook'] = yml_data['statementAllData']['requestList'][0]['pkAccountBook']
        yield request.param
        # 清理所有数据
        # dealData(get_find_voucher, get_del_voucher, get_headers, get_url, api_http, my_assert)

    @allure.story("利润表")
    def test_ProfitData(self, get_ProfitData_data, get_headers, get_url, api_http):
        assert_data = get_ProfitData_data.pop("assert_data")
        headers = get_headers(type=yml_data['getProfitData']['content_type'])
        url = get_url(yml_data['getProfitData']['path'])
        method = yml_data['getProfitData']['http_method']
        with allure.step("调用查询接口"):
            res = api_http(method, url, headers, get_ProfitData_data).json()
        # print(res)
        sheetList = res['financialStatementsts']
        get_ProfitData_data['assert_data'] = assert_data
        for my_assert in assert_data:
            for sheet in sheetList:
                if my_assert['name'] == sheet['name']:
                    # print(my_assert['name'])
                    assert my_assert['bigDecimalYearAll'] == sheet['bigDecimalYearAll']
                    assert my_assert['bigDecimalCurrentAll'] == sheet['bigDecimalCurrentAll']

    def test_deal_data(self, del_voucher, get_del_voucher, get_headers, get_url, api_http, my_assert,
                       test_find_voucher):
        # 处理数据 一、删除所有凭证
        pkVouchers = test_find_voucher
        for pkVoucher in pkVouchers:
            get_del_voucher['pkVoucher'] = pkVoucher  # 更新凭证主键
            del_voucher(get_del_voucher, get_headers, get_url, api_http, my_assert)

    def test_reset(self, get_reset_init_balance_data, get_headers, get_url, api_http, reset_init_balance):
        # 二 清除科目余额
        reset_init_balance(get_reset_init_balance_data, get_headers, get_url, api_http)

    def test_del_subject(self, delete_subject, get_delete_subject_data, get_headers, get_url, api_http, my_assert):
        # 三、删除新增的科目
        delete_subject(get_delete_subject_data, get_headers, get_url, api_http, my_assert)

    def test_del_contact(self, del_contacts, get_del_contacts_data, get_headers, get_url, api_http, my_assert):
        # 四、删除新增的客户
        del_contacts(get_del_contacts_data, get_headers, get_url, api_http, my_assert)
