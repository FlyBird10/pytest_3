from utils.generator import read_yml
from utils.DBUtil import Search, Del
import pytest
import allure
import os
import json

root_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "Question.yml"))


class Test_Question:
    DB_result = None
    @allure.step('校验接口响应代码和提示语')
    def my_assert(self, response, except_result):
        if response.status_code == 200:
            response = response.json()
            assert int(response['code']) == int(except_result['code'])
            assert response['message'] == except_result['message']
        else:
            print(response.content)

    @allure.step('数据准备和清理')
    @pytest.fixture(params=yml_data['AddQues']['requestList'])
    def get_add_question_data(self, request):
        sql = yml_data['AddQues']['sql']
        yield request.param
        # 删除接口插入的数据
        Del(sql['del1'].format(pkQuestion=DB_result[0][0]))
        Del(sql['del2'].format(pkQuestion=DB_result[0][0]))

    @allure.story("新增试题")
    def test_add_question(self, get_add_question_data, get_headers, get_url, api_http, request):
        global DB_result
        headers = get_headers(type=yml_data['AddQues']['content_type'])
        url = get_url(yml_data['AddQues']['path'])
        method = yml_data['AddQues']['http_method']
        except_result = get_add_question_data.pop('except_result')  # 取出请求参数对应的期望结果
        # 数据类型转json
        get_add_question_data_json = json.dumps(get_add_question_data)
        response = api_http(method, url, headers, get_add_question_data_json)
        self.my_assert(response, except_result)  # 校验响应
        questionContext = get_add_question_data['questionContext']
        # 查询数据库，校验数据是否被插入
        sql = yml_data['AddQues']['sql']['search']
        DB_result = Search(sql.format(questionContext=questionContext))
        assert len(DB_result) == 1  # 断言只插入了一条记录

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
