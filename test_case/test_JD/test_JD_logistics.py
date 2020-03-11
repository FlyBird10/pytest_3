from utils.generator import read_yml
import pytest
import allure
import os
import json

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "JD_logistics.yml"))


class Test_JD_logistics:
    @pytest.fixture(params=yml_data['platOrderList']['requestList'])
    def get_platOrderList_data(self, request):
        return request.param

    @allure.story("平台查询京东物流运单列表")
    def test_platOrderList(self, get_platOrderList_data, get_headers, get_url, api_http, my_assert):
        url = get_url(yml_data['platOrderList']['path'])
        headers = get_headers(type=yml_data['platOrderList']['content_type'])
        method = yml_data['platOrderList']['http_method']
        except_result = get_platOrderList_data.pop("except_result")
        response = api_http(method, url, headers, get_platOrderList_data)

        res_json = my_assert(response, except_result)['data']
        assert res_json['cjCount'] >= 0  # 待补差价订单数大于等于0
        assert res_json['tkCount'] >= 0  # 退款订单数大于等于0
        for i in res_json['orderList']:
            # assert i['sendAddress'] is not None
            try:
                assert i['sendAddress'] is not None  # 断言寄件地址不能为空
                assert i['receivesAddress'] is not None  # 断言收货地址不能为空
                assert i['wayBillCode'] is not None  # 运单号不为空
                assert i['xdCorpName'] is not None  # 下单公司名不为空
                assert i['createUserName'] is not None  # 提交人不为空
            except AssertionError:
                print('pkExpressDelivery:{pkExpressDelivery}'.format(
                    pkExpressDelivery=i['pkExpressDelivery']))  # 断言失败时打印订单主键
                assert 0  # 标记用例失败


