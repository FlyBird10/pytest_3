from utils.generator import read_yml
from utils.DBUtil import Search, Del
import pytest
import allure
import os
import json
import time
from urllib3 import encode_multipart_formdata

root_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "Paper.yml"))


@allure.feature("试卷库")
class Test_Paper:

    @allure.step('校验接口响应代码和提示语')
    def my_assert(self, response, except_result):
        if response.status_code == 200:
            response = response.json()
            assert int(response['code']) == int(except_result['code'])
            assert response['message'] == except_result['message']
            return response
        else:
            print(response.content)

    @pytest.fixture(params=yml_data['PaperList']['requestList'])
    def get_paper_list_data(self, request):
        return request.param

    @allure.story("查询试卷")
    def test_paper_list(self, get_headers, get_url, get_paper_list_data, api_http):
        headers = get_headers(type=yml_data['PaperList']['content_type'])
        url = get_url(yml_data['PaperList']['path'])
        method = yml_data['PaperList']['http_method']
        except_result = get_paper_list_data.pop("except_result")

        response = api_http(method, url, headers, get_paper_list_data)
        self.my_assert(response, except_result)
