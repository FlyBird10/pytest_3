from utils.generator import read_yml
import pytest
import allure
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_finalProof.yml"))
common = read_yml(os.path.join(finance_path, "common.yml"))


@allure.feature("期末凭证")
class TestFinalProof:
    @pytest.fixture(params=yml_data['findAll']['requestList'])
    def get_find_all_data(self, request):
        request.param['pkAccountBook'] = common['pkAccountBook']
        return request.param

    @allure.story("查询所有期末凭证模板")
    @pytest.mark.run(order=1)
    def test_find_all(self, get_find_all_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findAll']['content_type'])
        url = get_url(yml_data['findAll']['path'])
        method = yml_data['findAll']['http_method']
        except_result = get_find_all_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_all_data)
        with allure.step("断言接口响应成功"):
            global voucherTemplateList
            voucherTemplateList = my_assert(response, except_result)['data']
        get_find_all_data['except_result'] = except_result
        return voucherTemplateList

    @pytest.fixture(params=yml_data['generateVoucher']['requestList'])
    def get_generate_voucher_data(self, request, get_find_all_data, get_headers, get_url, api_http, my_assert,
                                  get_query_voucher_data):
        assert_data = request.param.pop("assert_data")  # 提取校验数据generateVoucher
        if request.param['date'] == 'findAll':
            request.param['date'] = yml_data['findAll']['requestList'][0]['date']
        # request.param['pkAccountBook'] = yml_data['findAll']['requestList'][0]['pkAccountBook']
        request.param['pkAccountBook'] = common['pkAccountBook']
        for voucherTemplate in voucherTemplateList:
            if request.param['pkVoucherTemplate'] == voucherTemplate['templateName']:
                request.param['pkVoucherTemplate'] = voucherTemplate['pkVoucherTemplate']
        yield request.param
        # 调用查询接口获取凭证PK
        get_find_all_data['date'] = request.param['date']
        voucherTemplates = self.test_find_all(get_find_all_data, get_headers, get_url, api_http, my_assert)
        for voucherTemplate in voucherTemplates:
            # 凭证模板一致时保存对应的凭证pk去查询凭证详情，与期望数据进行比对
            if voucherTemplate['pkVoucherTemplate'] == request.param['pkVoucherTemplate']:
                if voucherTemplate['voucherTemplateRecordVo'] is not None:
                    pkVoucher = voucherTemplate['voucherTemplateRecordVo']['pkVoucher']
                    get_query_voucher_data['pkVoucher'] = pkVoucher
                    resp = self.test_query_voucher_detail(get_query_voucher_data, get_headers, get_url, api_http, my_assert)
                    for voucherDetail in resp['data']['voucherDetailList']:  # 遍历凭证分录
                        for assert_detail in assert_data:  # 遍历校验数据
                            if voucherDetail['newName'] == assert_detail['newName']:
                                assert voucherDetail['explanation'] == assert_detail['explanation']
                                assert voucherDetail['amountDebit'] == assert_detail['amountDebit']
                                assert voucherDetail['amountCredit'] == assert_detail['amountCredit']

    @allure.story("生成期末凭证")
    @pytest.mark.run(order=2)
    def test_generate_voucher(self, get_generate_voucher_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['generateVoucher']['content_type'])
        url = get_url(yml_data['generateVoucher']['path'])
        method = yml_data['generateVoucher']['http_method']
        except_result = get_generate_voucher_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_generate_voucher_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)

    @pytest.fixture(params=yml_data['queryVoucherByPK']['requestList'])
    def get_query_voucher_data(self, request):
        return request.param

    @allure.story("查询凭证详情")
    @pytest.mark.run(order=3)
    def test_query_voucher_detail(self, get_query_voucher_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['queryVoucherByPK']['content_type'])
        url = get_url(yml_data['queryVoucherByPK']['path'])
        method = yml_data['queryVoucherByPK']['http_method']
        except_result = get_query_voucher_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_query_voucher_data)
        with allure.step("断言接口响应成功"):
            resp = my_assert(response, except_result)
        get_query_voucher_data['except_result'] = except_result
        return resp
