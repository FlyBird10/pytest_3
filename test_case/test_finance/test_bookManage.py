from utils.generator import read_yml
import pytest
import allure
import os
from FactoryData.ContactForCorpFac import get_subject

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_bookManage.yml"))

@pytest.mark.skip
@allure.feature("账套管理")
class TestFinanceBookManage:

    @pytest.fixture(params=yml_data['findAllBook']['requestList'])
    def get_find_book_manage_data(self, request):
        return request.param

    @allure.story("账套管理页面查询账套")
    @pytest.mark.run(order=1)
    @allure.severity('blocker')
    def test_find_book_manage(self, get_find_book_manage_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findAllBook']['content_type'])
        url = get_url(yml_data['findAllBook']['path'])
        method = yml_data['findAllBook']['http_method']
        except_result = get_find_book_manage_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_book_manage_data)
        with allure.step("断言接口响应成功"):
            resp = my_assert(response, except_result)
            bookList = resp['data']['pageBean']['items']  # 账套列表
            customerManagerSet = set()  # 账套的客户经理
            serviceManagerSet = set()  # 账套的客服经理
            userSet = set()  # 账套的记账会计
            for book in bookList:
                if book['customerManager'] is not None:
                    customerManagerSet.add(book['customerManager']['name'])
                if book['serviceManager'] is not None:
                    serviceManagerSet.add(book['serviceManager']['name'])
                if book['user'] is not None:
                    userSet.add(book['user']['name'])
                if book['checkStatus'] == 1:  # 已启用
                    assert book['accountingStandard'] is not None  # 会计准则不能为空
                    assert book['currency'] is not None  # 币种不能为空
                    assert book['tallyStatus'] is not None  # 记账状态不能为空
                    assert book['taxStatus'] is not None  # 报税状态不能为空
                assert book['customer'] is not None
            assert len(resp['data']['customerManagerList']) == len(customerManagerSet)  # 校验顶部备选项与列表保持一致
            # assert len(resp['data']['serviceManagerList']) == len(serviceManagerSet)  # 已提交bug
            assert len(resp['data']['userList']) == len(userSet)

    @pytest.fixture(params=yml_data['createBook']['requestList'])
    def get_create_book_data(self, request):
        request.param['accountBookName'] = get_subject()[0]['subjectName']  # 名称随机
        return request.param

    @allure.story("新建账套")
    @allure.severity('blocker')
    def test_create_book(self, get_create_book_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['createBook']['content_type'])
        url = get_url(yml_data['createBook']['path'])
        method = yml_data['createBook']['http_method']
        except_result = get_create_book_data.pop("except_result")
        with allure.step("调用新增接口"):
            response = api_http(method, url, headers, get_create_book_data)
        with allure.step("断言接口响应成功"):
            resp = my_assert(response, except_result)
        with allure.step("调用查询接口，校验新建成功"):
            pass
