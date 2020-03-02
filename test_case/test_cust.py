from utils.generator import read_yml
import pytest
import allure
from FactoryData.ContactForCorpFac import get_contact
import os
import json

# yml_data = read_yml("F:\\pytest_3\\data\\customer_my.yml")
root_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "customer_my.yml"))
pkCustomer = None


@allure.feature("客户模块")
class Test_customer():
    data_custo = yml_data['customer_my']

    @pytest.fixture(params=yml_data['customer_my']['requestList'])
    def get_data_customer_my(self, request):
        return request.param

    @pytest.mark.run(order=1)
    @pytest.mark.dependency()  # 被依赖
    def test_find_customer_my(self, get_headers, get_url, get_data_customer_my, api_http):
        """
        查询我的客户
        :param get_headers:
        :param get_url:
        :param get_data_customer_my:
        :param api_http:
        :return:
        """
        global pkCustomer
        headers = get_headers(type=yml_data['customer_my']['content_type'])
        # print(headers)
        url = get_url(yml_data['customer_my']['path'])
        method = yml_data['customer_my']['http_method']
        response = api_http(method, url, headers, get_data_customer_my)
        # print(response.json())
        print(response.headers)
        try:
            pkCustomer = response.json()['data']['customers']['object'][0]['pkCustomer']
        except Exception as e:
            print(e)
        print("find_customer_my方法中返回的客户主键：{}".format(pkCustomer))
        # assert 0


class Test_customer_dept:
    dic_data = yml_data['customer_dept']

    def test_customer_my_dept(self, get_headers, get_url, api_http):
        """
        查询我的客户页面筛选部门备选项
        :param get_headers:
        :param get_url:
        :param api_http:
        :return:
        """
        headers = get_headers(type=yml_data['customer_dept']['content_type'])
        url = get_url(yml_data['customer_dept']['path'])
        method = yml_data['customer_dept']['http_method']
        response = api_http(method, url, headers)
        print(response.json())
        print(response.headers)


@allure.story("客户联系人")
class Test_contact:
    # @allure.step("读取用例文件")
    dic_data = yml_data['add_contact']
    num = len(dic_data['requestList'])

    @allure.step('获取随机&依赖参数')
    @pytest.fixture(params=get_contact(num))
    def get_add_contact(self, request):
        global pkCustomer
        # @allure.step("获取依赖参数 pkCustomer")
        request.param['pkCustomer'] = pkCustomer
        return request.param

    @pytest.mark.run(order=2)
    @pytest.mark.dependency(depends=["test_find_customer_my"])  # 依赖谁
    def test_contact(self, get_add_contact, get_headers, get_url, api_http):
        """
        新增联系人
        :param get_add_contact:
        :return:
        """
        headers = get_headers(type=yml_data['add_contact']['content_type'])
        url = get_url(yml_data['add_contact']['path'])
        method = yml_data['add_contact']['http_method']
        # print(type(get_add_contact))
        get_add_contact = json.dumps(get_add_contact)  # dict转json
        response = api_http(method, url, headers, get_add_contact)
        print(get_add_contact)
        # print(response.headers)
        print(response.json())
