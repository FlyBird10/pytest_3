from utils.generator import read_yml
import pytest
import allure
import os
import json

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_voucher.yml"))


@allure.feature("凭证管理")
class TestVoucher:

    @allure.story("添加凭证页面新增科目")
    @pytest.mark.skip
    def test_add_one(self, get_add_one_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['addOne']['content_type'])
        url = get_url(yml_data['addOne']['path'])
        method = yml_data['addOne']['http_method']
        except_result = get_add_one_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_add_one_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)

    @allure.story("保存凭证")
    @pytest.mark.run(order=2)
    @allure.severity('blocker')
    # @pytest.mark.skip
    def test_save_voucher(self, get_save_voucher_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['addVoucher']['content_type'])
        url = get_url(yml_data['addVoucher']['path'])
        method = yml_data['addVoucher']['http_method']
        except_result = get_save_voucher_data.pop("except_result")
        # print(json.dumps(get_save_voucher_data))
        with allure.step("调用接口"):
            response = api_http(method, url, headers, get_save_voucher_data)
            # print(response)
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)

    @pytest.fixture(params=yml_data['addVoucher']['requestList'])
    def get_save_voucher_data(self, request, test_find_init6):
        # allInit6List = test_find_init6(get_find_init6_data, get_headers, get_url, api_http, my_assert)
        allInit6List = test_find_init6
        request.param['pkAccountBook'] = yml_data['findInit6']['requestList'][0]['pkAccountBook']
        for allInit6 in allInit6List:
            for voucherDetail in request.param['voucherDetailList']:
                if allInit6['subjectName'] == voucherDetail['initialBalance']['subjectName']:
                    voucherDetail['pkCurrency'] = allInit6['exchangeRate'][0]['tcurrency'][
                        'pkCurrency']
                    voucherDetail['pkInitialBalance'] = allInit6['pkInitialBalance']
                    voucherDetail['initialBalance'] = allInit6
                if allInit6['isWL'] is True:  # 科目是否启用往来
                    voucherDetail['pkInitContacts'] = allInit6['initContacts'][0]['pkInitContacts']  # 设置往来公司

        return request.param

    @pytest.fixture(params=yml_data['addOne']['requestList'])
    def get_add_one_data(self, request):
        request.param['pkAccountBook'] = yml_data['findInit6']['requestList'][0]['pkAccountBook']
        return request.param

    # 查询凭证
    @pytest.fixture(params=yml_data['searchVoucher']['requestList'])
    def get_find_voucher(self, request, get_del_voucher, get_headers, get_url, api_http, my_assert):
        request.param['pkAccountBook'] = yml_data['findInit6']['requestList'][0]['pkAccountBook']
        yield request.param
        # 查询完成后删除凭证
        # for pkVoucher in pkVouchers:
        #     self.del_voucher(get_del_voucher, get_headers, get_url, api_http, my_assert, pkVoucher)

    @allure.story("查询凭证")
    @pytest.mark.run(order=3)
    @allure.severity('blocker')
    def test_find_voucher(self, get_find_voucher, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['searchVoucher']['content_type'])
        url = get_url(yml_data['searchVoucher']['path'])
        method = yml_data['searchVoucher']['http_method']
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

    @pytest.fixture(params=yml_data['delVoucher']['requestList'])
    def get_del_voucher(self, request):
        # request.param['pkVoucher'] = pkVouchers[0]
        return request.param

    @allure.story("删除凭证")
    @pytest.mark.skip
    @pytest.mark.run(order=3)
    def del_voucher(self, get_del_voucher, get_headers, get_url, api_http, my_assert, pkVoucher):
        headers = get_headers(type=yml_data['delVoucher']['content_type'])
        url = get_url(yml_data['delVoucher']['path'])
        method = yml_data['delVoucher']['http_method']
        get_del_voucher['pkVoucher'] = pkVoucher
        except_result = get_del_voucher.pop("except_result")
        with allure.step("调用接口"):
            response = api_http(method, url, headers, get_del_voucher)
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)
        get_del_voucher['except_result'] = except_result
