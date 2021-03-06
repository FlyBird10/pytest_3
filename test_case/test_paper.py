from utils.generator import read_yml
from utils.DBUtil import Search, Del
import pytest
import allure
import os

root_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "Paper.yml"))


@allure.feature("试卷库")
class Test_Paper:

    @pytest.fixture(params=yml_data['PaperList']['requestList'])
    def get_paper_list_data(self, request):
        return request.param

    @allure.story("查询试卷")
    def test_paper_list(self, get_headers, get_url, get_paper_list_data, api_http, my_assert):
        headers = get_headers(type=yml_data['PaperList']['content_type'])
        url = get_url(yml_data['PaperList']['path'])
        method = yml_data['PaperList']['http_method']
        expect_result = get_paper_list_data.pop("expect_result")

        response = api_http(method, url, headers, get_paper_list_data)
        my_assert(response, expect_result)

    @pytest.fixture(params=yml_data['CopyPaper']['requestList'])
    def get_copy_paper_data(self, request, get_headers):
        if request.param['pkPaper'] == 'sql':
            with allure.step("查询数据库获取试卷pk"):
                pkCorp = get_headers()['pkmanagercorp']
                sql = yml_data['CopyPaper']['sql']['allPaper']
                pkPaperList = Search(sql.format(pkCorp=pkCorp))
                allure.attach("使用查询到的第一个PK")
                request.param['pkPaper'] = pkPaperList[0][0]
        return request.param

    @allure.story("复制试卷")
    def test_copy_paper(self, get_headers, get_url, get_copy_paper_data, api_http, my_assert):
        headers = get_headers()
        method = yml_data['CopyPaper']['http_method']
        url = get_url(yml_data['CopyPaper']['path'])
        expect_result = get_copy_paper_data.pop("expect_result")

        response = api_http(method, url, headers, get_copy_paper_data)

        my_assert(response, expect_result)
