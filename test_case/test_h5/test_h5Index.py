from utils.generator import read_yml
from utils.DBUtil import Search_redis, Del, Search
import pytest
import allure
import os
import json
import time

root_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "h5_index.yml"))


class TestIndex:

    @pytest.fixture(params=yml_data['bind']['requestList'])
    def get_band_data(self, request):
        return request.param

    @allure.story("查询微信是否被绑定")
    @pytest.mark.run(order=1)
    def test_check_bind_phone(self, get_band_data, get_headers_Notoken, get_url, api_http, my_assert):
        global token, pkCorp, pkManagerCorp
        headers = get_headers_Notoken(type=yml_data['bind']['content_type'])
        url = get_url(yml_data['bind']['path'])
        method = yml_data['bind']['http_method']
        except_result = get_band_data.pop("except_result")
        response = api_http(method, url, headers, get_band_data)
        resp = my_assert(response, except_result)
        if resp['data']:  # 登录成功时更新token
            token = resp['data']['tokenInfo']['access_token']
            pkCorp = resp['data']['corpInfo'][0]['pkCorp']
            pkManagerCorp = get_band_data['pkManagerCorp']
            return token

    @pytest.fixture(params=yml_data['sendSMS']['requestList'])
    def get_phoneCode_data(self, request):
        return request.param

    @pytest.mark.run(order=1)
    @pytest.mark.skip
    def test_send_sms(self, get_phoneCode_data, get_headers_Notoken, get_url, api_http, my_assert):
        headers = get_headers_Notoken()
        url = get_url(yml_data['sendSMS']['path'])
        method = yml_data['sendSMS']['http_method']
        except_result = get_phoneCode_data.pop("except_result")
        response = api_http(method, url, headers, get_phoneCode_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['bindPhone']['requestList'])
    def get_bind_phone_data(self, request):
        if request.param['code'] == 'sql':
            phone = request.param['phone']
            searchSql = str(phone) + yml_data['bindPhone']['sql']['searchCode']
            code = int(Search_redis(searchSql))
            request.param['code'] = code
        yield request.param
        if request.param['except_result']['code'] == 0:
            # 可能绑定成功的账号清除绑定相关信息
            searchPkUser = yml_data['bindPhone']['sql']['searchPkUser']
            pkUser = Search(searchPkUser)[0][0]
            delBindData1 = yml_data['bindPhone']['sql']['delBindData1'].format(pkUser=pkUser)
            delBindData2 = yml_data['bindPhone']['sql']['delBindData2'].format(pkUser=pkUser)
            Del(delBindData1)
            Del(delBindData2)

    @pytest.mark.skip
    def test_bind_phone(self, get_bind_phone_data, get_headers_Notoken, get_url, api_http, my_assert):
        headers = get_headers_Notoken(type=yml_data['bindPhone']['content_type'])
        url = get_url(yml_data['bindPhone']['path'])
        method = yml_data['bindPhone']['http_method']
        except_result = get_bind_phone_data.pop("except_result")
        response = api_http(method, url, headers, get_bind_phone_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['switchCorp']['requestList'])
    def get_switch_corp_data(self, request):
        request.param['pkCorp'] = pkCorp
        return request.param

    def test_switch_corp(self, get_switch_corp_data, get_headers_h5, get_url, api_http, my_assert):
        headers = get_headers_h5(token=token, type=yml_data['switchCorp']['content_type'])
        method = yml_data['switchCorp']['http_method']
        except_result = get_switch_corp_data.pop("except_result")
        url = get_url(yml_data['switchCorp']['path'])
        response = api_http(method, url, headers, get_switch_corp_data)

        my_assert(response, except_result)
