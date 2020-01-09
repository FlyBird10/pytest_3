from utils.generator import read_yml
import pytest
import allure
import os
import json

root_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "Question.yml"))


class Test_Question:
    def my_assert(self, response, except_result):
        if response.status_code == 200:
            response = response.json()
            assert response['code'] == except_result['code']
            assert response['message'] == except_result['message']
        else:
            print(response.content)

    @pytest.fixture(params=yml_data['AddQues']['requestList'])
    def get_add_question_data(self, request):
        return request.param

    @allure.story("新增试题")
    def test_add_question(self, get_add_question_data, get_headers, get_url, api_http):
        headers = get_headers(type=yml_data['AddQues']['content_type'])
        url = get_url(yml_data['AddQues']['path'])
        method = yml_data['AddQues']['http_method']
        except_result = get_add_question_data.pop('except_result')  # 取出请求参数对应的期望结果
        # 数据类型转json
        get_add_question_data = json.dumps(get_add_question_data)
        response = api_http(method, url, headers, get_add_question_data)
        self.my_assert(response, except_result)  # 校验响应

    @pytest.fixture(params=yml_data['QuesList']['requestList'])
    def get_list_ques_data(self, request):
        return request.param

    @allure.story('显示试题')
    def test_list_question(self, get_headers, get_url, api_http, get_list_ques_data):
        headers = get_headers(type=yml_data['QuesList']['content_type'])
        url = get_url(yml_data['QuesList']['path'])
        method = yml_data['QuesList']['http_method']
        except_result = get_list_ques_data.pop('except_result')
        get_list_ques_data = json.dumps(get_list_ques_data)
        response = api_http(method, url, headers, get_list_ques_data)
        self.my_assert(response, except_result)
