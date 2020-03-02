from utils.generator import read_yml
from utils.DBUtil import Search_redis, Del, Search
import pytest
import allure
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "h5_shoppingMall.yml"))


@allure.feature("H5-商城")
class Test_ShoppingMall:

    @pytest.fixture(params=yml_data['mall']['requestList'])
    def get_shopping_mall_data(self, request, get_Token_h5):
        if request.param['pkCorps'] == 'tokenGroup':
            request.param['pkCorps'] = get_Token_h5(isGroup=True)['pkManagerCorp']
        elif request.param['pkCorps'] == 'tokenCorp':
            request.param['pkCorps'] = get_Token_h5()['pkManagerCorp']
        return request.param

    @allure.story("查询商城商品")
    @pytest.mark.run(order=1)
    def test_order_info(self, get_shopping_mall_data, get_headers_h5, get_url, api_http, my_assert):
        url = get_url(yml_data['mall']['path'])
        headers = get_headers_h5(type=yml_data['mall']['content_type'])
        method = yml_data['mall']['http_method']
        except_result = get_shopping_mall_data.pop("except_result")
        response = api_http(method, url, headers, get_shopping_mall_data)
        response_json = my_assert(response, except_result)
        product_list = response_json['data']
        assert len(product_list) > 0  # 校验商城至少有一个商品
        global product_pk
        product_pk = {}
        for i in product_list:
            if i['isSingle'] == '0':  # 单品
                product_pk['single'] = i['pkProductH']
                product_pk['singleCorp'] = i['pkCorp']
            elif i['isSingle'] == '1':  # 套餐
                product_pk['complex'] = i['pkProductH']
                product_pk['complexCorp'] = i['pkCorp']

    @pytest.fixture(params=yml_data['productDetail']['requestList'])
    def get_product_detail_data(self, request):
        if request.param['pkProductH'] == 'single':
            request.param['pkProductH'] = product_pk['single']
        elif request.param['pkProductH'] == 'complex':
            request.param['pkProductH'] = product_pk['complex']

        return request.param

    @allure.story("查询商品详情")
    def test_order_detail(self, get_product_detail_data, get_headers_h5, get_url, api_http, my_assert):
        url = get_url(yml_data['productDetail']['path'])
        headers = get_headers_h5(type=yml_data['productDetail']['content_type'])
        method = yml_data['productDetail']['http_method']
        except_result = get_product_detail_data.pop("except_result")
        response = api_http(method, url, headers, get_product_detail_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['productComment']['requestList'])
    def get_product_comment_data(self, request):
        if request.param['pkProductH'] == 'single':
            request.param['pkCorp'] = product_pk['singleCorp']
            request.param['pkProductH'] = product_pk['single']
        elif request.param['pkProductH'] == 'complex':
            request.param['pkCorp'] = product_pk['complexCorp']
            request.param['pkProductH'] = product_pk['complex']

        return request.param

    @allure.story("查询商品评价")
    def test_order_comment(self, get_product_comment_data, get_headers_h5, get_url, api_http, my_assert):
        url = get_url(yml_data['productComment']['path'])
        headers = get_headers_h5(type=yml_data['productComment']['content_type'])
        method = yml_data['productComment']['http_method']
        except_result = get_product_comment_data.pop("except_result")
        response = api_http(method, url, headers, get_product_comment_data)
        my_assert(response, except_result)
