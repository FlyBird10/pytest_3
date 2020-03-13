from utils.generator import read_yml
import pytest
import allure
import os
from FactoryData.ContactForCorpFac import get_subject

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_assistAccoun.yml"))


@allure.feature("辅助核算")
class TestAssisAccoun:

    @allure.story("添加客户")
    @pytest.mark.run(order=1)
    @allure.severity('blocker')
    def test_add_contacts(self, get_add_contacts_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['addContacts']['content_type'])
        url = get_url(yml_data['addContacts']['path'])
        method = yml_data['addContacts']['http_method']
        except_result = get_add_contacts_data.pop("except_result")
        with allure.step("调用add接口"):
            response = api_http(method, url, headers, get_add_contacts_data)
        get_add_contacts_data['except_result'] = except_result
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)

    @allure.story("查询辅助核算列表")
    @pytest.mark.run(order=2)
    @allure.severity('blocker')
    def test_find_all_contacts(self, get_find_all_contacts_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findContacts']['content_type'])
        url = get_url(yml_data['findContacts']['path'])
        method = yml_data['findContacts']['http_method']
        except_result = get_find_all_contacts_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_all_contacts_data)
        get_find_all_contacts_data['except_result'] = except_result
        with allure.step("断言接口响应成功"):
            global projectList
            projectList = my_assert(response, except_result)['data']
            print(projectList)
        return projectList

    @pytest.fixture(params=yml_data['delContacts']['requestList'])
    def get_del_contacts_data(self, request):
        print(projectList)
        request.param['pkContacts'] = projectList[0]['pkContacts']
        projectList.pop(0)
        # print(request.param)
        return request.param

    @allure.story("删除客户")
    @pytest.mark.skip
    @allure.severity('blocker')
    def test_del_contacts(self, get_del_contacts_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['delContacts']['content_type'])
        url = get_url(yml_data['delContacts']['path'])
        method = yml_data['delContacts']['http_method']
        except_result = get_del_contacts_data.pop("except_result")
        with allure.step("调用del接口"):
            response = api_http(method, url, headers, get_del_contacts_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, except_result)