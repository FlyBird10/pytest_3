from utils.generator import read_yml
from utils.DBUtil import Search_redis, Del, Search
import pytest
import allure
import os
import json
import time

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "h5_order.yml"))


class Test_Order:
    @pytest.fixture(params=yml_data['allOrderList']['requestList'])
    def get_order_info_data(self, request, get_Token_h5):
        if request.param['pkManagerCorp'] == 'tokenGroup':
            request.param['pkManagerCorp'] = get_Token_h5(isGroup=True)['pkManagerCorp']
            # 增加此变量以便用例确定取值
            request.param['isGroup'] = True
            print('pkManagerCorp:====', request.param['pkManagerCorp'])
        elif request.param['pkManagerCorp'] == 'tokenCorp':
            request.param['isGroup'] = False
            request.param['pkManagerCorp'] = get_Token_h5()['pkManagerCorp']
        return request.param

    @allure.story("查询订单-非群组")
    def test_order_info(self, get_order_info_data, get_headers_h5, get_url, api_http, my_assert):
        url = get_url(yml_data['allOrderList']['path'])
        isGroup = get_order_info_data.pop("isGroup")
        if isGroup:
            headers = get_headers_h5(isGroup=True)
        else:
            headers = get_headers_h5()
        method = yml_data['allOrderList']['http_method']
        except_result = get_order_info_data.pop("except_result")
        response = api_http(method, url, headers, get_order_info_data)

        my_assert(response, except_result)


