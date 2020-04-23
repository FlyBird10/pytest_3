from utils.generator import read_yml
import pytest
import allure
import os

# from test_case.test_finance.conftest import test_find_init6

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_asset.yml"))
common = read_yml(os.path.join(finance_path, "common.yml"))


# @pytest.mark.skip
@allure.feature("固定资产")
class TestAsset:

    @pytest.fixture(params=yml_data['findAssetCard']['requestList'])
    def get_find_asset_class_data(self, request):
        request.param['pkAccountBook'] = common['pkAccountBook']
        return request.param

    @allure.story("查询固定资产类别")
    @pytest.mark.run(order=1)
    @allure.severity('blocker')
    # @pytest.mark.skip
    def test_find_asset_class(self, get_find_asset_class_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findAssetCard']['content_type'])
        url = get_url(yml_data['findAssetCard']['path'])
        method = yml_data['findAssetCard']['http_method']
        expect_result = get_find_asset_class_data.pop("expect_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_asset_class_data)
        with allure.step("断言接口响应成功"):
            global allAssetClassList
            allAssetClassList = my_assert(response, expect_result)['data']
            # print(allAssetClassList)

    @pytest.fixture(params=yml_data['addAsset']['requestList'])
    def get_add_asset_data(self, request, test_find_init6):
        request.param['pkAccountBook'] = common['pkAccountBook']
        for allAssetClass in allAssetClassList:
            if allAssetClass['className'] == request.param['className']:
                # request.param['createDate'] = allAssetClass['createDate']
                request.param['operator'] = allAssetClass['operator']
                request.param['pkAccountBook'] = allAssetClass['pkAccountBook']
                request.param['pkManageCorp'] = allAssetClass['pkManageCorp']
                request.param['scrapValue'] = allAssetClass['scrapValue']
                request.param['pkCostsAccount'] = allAssetClass['pkCostsAccount']
                request.param['pkAssetClass'] = allAssetClass['pkAssetClass']
                request.param['pkDepreciationAccount'] = allAssetClass['pkDepreciationAccount']
        for allInit6 in test_find_init6:
            if request.param['costsAccount'] == allInit6['subjectName']:
                request.param['pkCostsAccount'] = allInit6['pkInitialBalance']

        return request.param

    @allure.story("添加固定资产")
    @pytest.mark.run(order=2)
    @allure.severity('blocker')
    # @pytest.mark.skip
    def test_add_asset(self, get_add_asset_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['addAsset']['content_type'])
        url = get_url(yml_data['addAsset']['path'])
        method = yml_data['addAsset']['http_method']
        expect_result = get_add_asset_data.pop("expect_result")
        with allure.step("调用添加接口"):
            response = api_http(method, url, headers, get_add_asset_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, expect_result)

    @pytest.fixture(params=yml_data['findAsset']['requestList'])
    def get_find_asset_data(self, request):
        request.param['pkAccountBook'] = common['pkAccountBook']
        return request.param

    @allure.story("查询固定资产")
    @pytest.mark.run(order=3)
    def test_find_asset(self, get_find_asset_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findAsset']['content_type'])
        url = get_url(yml_data['findAsset']['path'])
        method = yml_data['findAsset']['http_method']
        expect_result = get_find_asset_data.pop("expect_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_asset_data)
        with allure.step("断言接口响应成功"):
            global allAssetList
            allAssetList = my_assert(response, expect_result)['data']
            for allAsset in allAssetList:
                # 校验资产状态
                if allAsset['assetsName'] in ("资产B", "资产A"):
                    assert allAsset['status'] == 1
                elif allAsset['assetsName'] == '资产C':
                    assert allAsset['status'] == 3

    # @pytest.fixture(params=yml_data['delAsset']['requestList'])
    # def get_del_asset_data(self, request):
    #     for allAsset in allAssetList:
    #         if allAsset['assetsName'] == '测试':
    #             request.param['pkAssetsCard'] = allAsset['pkAssetsCard']
    #     return request.param
    #
    # @allure.story("删除固定资产")
    # @pytest.mark.run(order=4)
    # @pytest.mark.skip
    # def test_del_asset(self, get_del_asset_data, get_headers, get_url, api_http, my_assert):
    #     headers = get_headers(type=yml_data['delAsset']['content_type'])
    #     url = get_url(yml_data['delAsset']['path'])
    #     method = yml_data['delAsset']['http_method']
    #     expect_result = get_del_asset_data.pop("expect_result")
    #     # print(get_del_asset_data)
    #     with allure.step("调用删除接口"):
    #         response = api_http(method, url, headers, get_del_asset_data)
    #     with allure.step("断言接口响应成功"):
    #         my_assert(response, expect_result)
    @pytest.fixture(params=yml_data['AddIntangibleAsset']['requestList'])
    def get_add_intangibleAsset_data(self, request, get_intangibleAssetCategory):
        assert len(get_intangibleAssetCategory) > 0, "没有无形资产的资产类别"
        request.param['pkAccountBook'] = common['pkAccountBook']
        for category in get_intangibleAssetCategory:
            if category['categoryName'] == '土地使用权':
                request.param['accumulatedAccount'] = category['accumulatedAccount']
                request.param['accumulatedAccountCode'] = category['accumulatedAccountCode']
                request.param['accumulatedAccountName'] = category['accumulatedAccountName']
                request.param['accumulatedInitialBalance'] = category['accumulatedInitialBalance']
                request.param['expenseAccount'] = category['expenseAccount']
                request.param['expenseAccountCode'] = category['expenseAccountCode']
                request.param['expenseAccountName'] = category['expenseAccountName']
                request.param['expenseInitContacts'] = category['expenseInitContacts']
                request.param['expenseInitialBalance'] = category['expenseInitialBalance']
                request.param['lifeTime'] = category['durableLife']
                request.param['pkIntangibleAssetsCategory'] = category['pkIntangibleAssetsCategory']
        return request.param

    @allure.story("添加无形资产")
    def test_add_intangibleAsset(self, get_add_intangibleAsset_data, get_headers, get_url, api_http, my_assert, ):
        headers = get_headers(type=yml_data['AddIntangibleAsset']['content_type'])
        url = get_url(yml_data['AddIntangibleAsset']['path'])
        method = yml_data['AddIntangibleAsset']['http_method']
        expect_result = get_add_intangibleAsset_data.pop("expect_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_add_intangibleAsset_data)
        with allure.step("断言接口响应成功"):
            my_assert(response, expect_result)
