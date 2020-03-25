from utils.generator import read_yml
import pytest
import allure
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "platform.yml"))


@allure.feature("类别配置")
class TestPlat:
    @pytest.fixture(params=yml_data['findInit']['requestList'])
    def get_find_init_data(self, request):
        return request.param

    @allure.story("查询科目")
    @pytest.mark.run(order=1)
    def test_find_init(self, get_find_init_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findInit']['content_type'])
        url = get_url(yml_data['findInit']['path'])
        method = yml_data['findInit']['http_method']
        except_result = get_find_init_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_init_data)
        with allure.step("断言接口响应成功"):
            global allInit6List
            allInit6List = my_assert(response, except_result)['data']

    @pytest.fixture(params=yml_data['insertSubjectCategory']['requestList'])
    def get_insert_category_data(self, request):
        for allInit6 in allInit6List:
            if allInit6['subjectName'] == request.param['subjectName'] and request.param['subjectCode'] == 'search':
                request.param['subjectCode'] = allInit6['subjectCode']
        return request.param

    @allure.story("新增类别")
    @pytest.mark.run(order=2)
    @allure.severity('blocker')
    # @pytest.mark.skip
    def test_insert_category(self, get_insert_category_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['insertSubjectCategory']['content_type'])
        url = get_url(yml_data['insertSubjectCategory']['path'])
        method = yml_data['insertSubjectCategory']['http_method']
        except_result = get_insert_category_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_insert_category_data)
        with allure.step("断言接口响应成功"):
            global allAssetClassList
            allAssetClassList = my_assert(response, except_result)['data']
