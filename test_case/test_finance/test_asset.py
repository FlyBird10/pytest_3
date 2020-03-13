from utils.generator import read_yml
import pytest
import allure
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_asset.yml"))


@allure.feature("资产")
class TestAsset:

    @pytest.fixture(params=yml_data['findAssetCard']['requestList'])
    def get_find_asset_class_data(self, request):
        return request.param

    @allure.story("查询科目及期初列表")
    @pytest.mark.run(order=1)
    @allure.severity('blocker')
    def test_find_init_balance(self, get_find_asset_class_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['findAssetCard']['content_type'])
        url = get_url(yml_data['findAssetCard']['path'])
        method = yml_data['findAssetCard']['http_method']
        except_result = get_find_asset_class_data.pop("except_result")
        with allure.step("调用查询接口"):
            response = api_http(method, url, headers, get_find_asset_class_data)
        with allure.step("断言接口响应成功"):
            global allAssetClassList
            allAssetClassList = my_assert(response, except_result)['data']
            print(allAssetClassList)