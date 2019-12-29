from utils.generator import read_yml
import pytest
import requests
import allure

yml_data = read_yml("F:\\pytest_3\\data\\customer_my.yml")


class Test_customer_my:
    dic_data = yml_data['customer_my']
    params = dic_data['requestList']

    @allure.step("获取请求参数")
    @pytest.fixture(params=dic_data['requestList'])
    def get_customer_my(self, request):
        return request.param

    @allure.step('获取请求属性')
    def http(self, get_headers, get_url):
        http = {}
        http['headers'] = get_headers(type=yml_data['customer_my']['content_type'])
        http['url'] = get_url(yml_data['customer_my']['path'])
        http['method'] = yml_data['customer_my']['http_method']
        return http

    @allure.feature('客户中心')
    @allure.testcase('查询我的客户')
    def test_customer_my(self, get_headers, get_url, get_customer_my):
        http = self.http(get_headers, get_url)
        if http['method'] == "post":
            response = requests.post(http['url'], headers=http['headers'], data=get_customer_my)
        else:
            response = requests.post(http['url'], headers=http['headers'], data=get_customer_my)
        print(response.json())


class Test_customer_dept:
    dic_data = yml_data['customer_dept']
    params = dic_data['requestList']

    @pytest.fixture(params=dic_data['requestList'])
    def get_customer_dept(self, request):
        return request.param

    def http(self, get_headers, get_url):
        http = {}
        http['headers'] = get_headers(type=yml_data['customer_dept']['content_type'])
        http['url'] = get_url(yml_data['customer_dept']['path'])
        http['method'] = yml_data['customer_dept']['http_method']
        return http

    @allure.feature('客户中心')
    @allure.testcase('我的客户——客户归属部门备选项')
    def test_customer_dept(self, get_headers, get_url):
        http = self.http(get_headers, get_url)
        if http['method'] == "post":
            response = requests.post(http['url'], headers=http['headers'])
        else:
            response = requests.post(http['url'], headers=http['headers'])
        print(response.json())
