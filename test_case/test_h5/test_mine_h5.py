from utils.generator import read_yml
from utils.DBUtil import Search_redis, Del, Search
import pytest
import allure
import os
import json
import time

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "h5_mine.yml"))


class Test_Mine:
    @pytest.fixture(params=yml_data['userInfo']['requestList'])
    def get_user_info_data(self, request, get_Token_h5):
        # if request.param['code'] == 'token':
        #     request.param['code'] = get_Token_h5()['pkUser']
        return request.param

    @allure.story("查询个人信息")
    def test_user_info(self, get_user_info_data, get_headers_h5, get_url, api_http, my_assert):
        url = get_url(yml_data['userInfo']['path'])
        headers = get_headers_h5()
        method = yml_data['userInfo']['http_method']
        except_result = get_user_info_data.pop("except_result")
        response = api_http(method, url, headers, get_user_info_data)

        my_assert(response, except_result)
