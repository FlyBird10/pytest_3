from utils.generator import read_yml
import pytest
import allure
import os
from FactoryData.ContactForCorpFac import get_subject
from utils.DBUtil import Del, Search

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_assistAccoun.yml"))


@allure.feature("辅助核算")
class TestAssisAccoun:

    @pytest.fixture(params=yml_data['addContacts']['requestList'])
    def get_add_contacts_data(self, request):
        # 数据准备
        request.param['pkAccountBook'] = yml_data['findContacts']['requestList'][0]['pkAccountBook']
        request.param['contactsCrop'] = get_subject()[0]['subjectName']
        return request.param

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
