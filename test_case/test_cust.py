from utils.generator import read_yml
import pytest
import allure
from FactoryData.ContactForCorpFac import get_contact

yml_data = read_yml("F:\\pytest_3\\data\\customer_my.yml")
pkCustomer = None


class Test_customer:
    data_custo = yml_data['customer_my']

    @pytest.fixture(params=yml_data['customer_my']['requestList'])
    def get_data_customer_my(self, request):
        return request.param

    @pytest.mark.run(order=1)
    @pytest.mark.dependency()  # 被依赖
    def test_find_customer_my(self, get_headers, get_url, get_data_customer_my, api_http):
        global pkCustomer
        headers = get_headers(type=yml_data['customer_my']['content_type'])
        print(headers)
        url = get_url(yml_data['customer_my']['path'])
        method = yml_data['customer_my']['http_method']
        response = api_http(method, url, headers, get_data_customer_my)
        print(response.json())
        pkCustomer = response.json()['data']['customers']['object'][0]['pkCustomer']
        print("find_customer_my方法中返回的客户主键：{}".format(pkCustomer))
        # assert 0


class Test_customer_dept1:
    dic_data = yml_data['customer_dept']
    print(dic_data['requestList'])

    @pytest.fixture(params=dic_data['requestList'])
    def get_customer_dept(self, request):
        return request.param

    def test_customer_my_dept(self, get_headers, get_url, api_http):
        headers = get_headers(type=yml_data['customer_dept']['content_type'])
        url = get_url(yml_data['customer_dept']['path'])
        method = yml_data['customer_dept']['http_method']
        response = api_http(method, url, headers)
        print(response.json())


class Test_contact:
    dic_data = yml_data['add_contact']
    num = len(dic_data['requestList'])

    @allure.step('获取随机参数')
    @pytest.fixture(params=get_contact(num))
    def get_add_contact(self, request):
        global pkCustomer
        # @allure.step("获取依赖参数 pkCustomer")
        request.param['pkCustomer'] = pkCustomer
        return request.param

    @pytest.mark.run(order=2)
    @pytest.mark.dependency(depends=["test_find_customer_my"])  # 依赖谁
    def test_contact(self, get_add_contact):
        """
        新增联系人
        :param get_add_contact:
        :return:
        """
        print(get_add_contact)

