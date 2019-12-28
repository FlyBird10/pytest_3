from utils.generator import read_yml
import pytest

yml_data = read_yml("E:\\pytest_3\\data\\customer_my.yml")


class Test_customer:
    data_custo = yml_data['customer_my']

    @pytest.fixture(params=yml_data['customer_my']['requestList'])
    def get_data_customer_my(self, request):
        return request.param

    def test_find_customer_my(self, get_headers, get_url, get_data_customer_my, api_http):
        headers = get_headers(type=yml_data['customer_my']['content_type'])
        url, account = get_url(yml_data['customer_my']['path'])
        method = yml_data['customer_my']['http_method']
        response = api_http(method, url, headers, get_data_customer_my)
        print(response.json())


class Test_customer_dept1:
    dic_data = yml_data['customer_dept']
    print(dic_data['requestList'])

    @pytest.fixture(params=dic_data['requestList'])
    def get_customer_dept(self, request):
        return request.param

    def test_customer_my_dept(self, get_headers, get_url, api_http):
        headers = get_headers(type=yml_data['customer_dept']['content_type'])
        url, account = get_url(yml_data['customer_dept']['path'])
        method = yml_data['customer_dept']['http_method']
        response = api_http(method, url, headers)
        # if response.status_code != 200:
        #     print(response.request.headers)
        #     print(response.request.url)
        print(response.json())
