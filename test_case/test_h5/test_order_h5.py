from utils.generator import read_yml
from utils.DBUtil import Search_redis, Del, Search
import pytest
import allure
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "h5_order.yml"))


@allure.feature("H5-我的订单")
class Test_Order:

    @pytest.fixture(params=yml_data['allOrderList']['requestList'])
    def get_order_info_data(self, request, get_Token_h5):
        if request.param['pkManagerCorp'] == 'tokenGroup':
            request.param['pkManagerCorp'] = get_Token_h5(isGroup=True)['pkManagerCorp']
            # 增加此变量以便用例确定取值
            request.param['isGroup'] = True
            # print('pkManagerCorp:====', request.param['pkManagerCorp'])
        elif request.param['pkManagerCorp'] == 'tokenCorp':
            request.param['isGroup'] = False
            request.param['pkManagerCorp'] = get_Token_h5()['pkManagerCorp']
        return request.param

    @allure.story("查询订单列表")
    @pytest.mark.run(order=1)
    def test_order_info(self, get_order_info_data, get_headers_h5, get_url, api_http, my_assert):
        global order
        order = {}
        url = get_url(yml_data['allOrderList']['path'])
        isGroup = get_order_info_data.pop("isGroup")
        with allure.step("查询群组和非群组下的订单"):
            if isGroup:
                headers = get_headers_h5(isGroup=True, type=yml_data['allOrderList']['content_type'])
            else:
                headers = get_headers_h5(type=yml_data['allOrderList']['content_type'])
        method = yml_data['allOrderList']['http_method']
        except_result = get_order_info_data.pop("except_result")
        response = api_http(method, url, headers, get_order_info_data)
        response_json = my_assert(response, except_result)
        orderData = response_json['data']
        if len(orderData) > 0:
            for i in orderData:
                if i['status'] == 1:
                    order['notPay'] = i['pkOrderInfo']
                    order['notPayCode'] = i['orderCode']
                elif i['status'] == 2:
                    order['doing'] = i['pkOrderInfo']
                    order['doingCode'] = i['orderCode']
                elif i['status'] == 5:
                    order['installments'] = i['pkOrderInfo']
                    order['installmentsCode'] = i['orderCode']
                elif i['status'] == 3:
                    order['cancel'] = i['pkOrderInfo']
                    order['cancelCode'] = i['orderCode']
                elif i['status'] == 6:
                    order['done'] = i['pkOrderInfo']
                    order['doneCode'] = i['orderCode']
        print(order)

    @pytest.fixture(params=yml_data['orderDetail']['requestList'])
    def get_order_detail_data(self, request):
        if request.param['pkOrderInfo'] == 'notPay':
            request.param['pkOrderInfo'] = order['notPay']
        elif request.param['pkOrderInfo'] == 'installments':
            request.param['pkOrderInfo'] = order['installments']
        elif request.param['pkOrderInfo'] == 'doing':
            request.param['pkOrderInfo'] = order['doing']
        elif request.param['pkOrderInfo'] == 'done':
            request.param['pkOrderInfo'] = order['done']
        elif request.param['pkOrderInfo'] == 'cancel':
            request.param['pkOrderInfo'] = order['cancel']
        return request.param

    @allure.story("订单详情")
    def test_order_detail(self, get_order_detail_data, get_headers_h5, get_url, api_http, my_assert):
        url = get_url(yml_data['orderDetail']['path'])
        headers = get_headers_h5()
        method = yml_data['orderDetail']['http_method']
        except_result = get_order_detail_data.pop("except_result")
        response = api_http(method, url, headers, get_order_detail_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['orderComments']['requestList'])
    def get_order_comment_data(self, request):
        with allure.step("获取已完成订单的pk"):
            if request.param['pkOrderInfo'] == 'done':
                request.param['pkOrderInfo'] = order['done']
        return request.param

    @allure.story("提交评论")
    def test_order_comment(self, get_order_comment_data, get_headers_h5, get_url, api_http, my_assert):
        url = get_url(yml_data['orderComments']['path'])
        headers = get_headers_h5(type=yml_data['orderComments']['content_type'])
        method = yml_data['orderComments']['http_method']
        except_result = get_order_comment_data.pop("except_result")
        # get_order_comment_data = json.dumps(get_order_comment_data)  # dict转json
        response = api_http(method, url, headers, get_order_comment_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['orderDel']['requestList'])
    def get_order_del_data(self, request):
        if request.param['pkOrderInfo'] == 'cancel':
            request.param['pkOrderInfo'] = order['cancel']
            request.param['orderCode'] = order['cancelCode']
        elif request.param['pkOrderInfo'] == 'done':
            request.param['pkOrderInfo'] = order['done']
            request.param['orderCode'] = order['doneCode']
        print(request.param)
        update_deleted_order = yml_data['orderDel']['sql']['update_deleted_order'].format(
            pkOrderInfo=request.param['pkOrderInfo'])
        # print('del sql ===', update_deleted_order)
        yield request.param  # yield之后的语句用于数据清理，在用例执行完之后执行

        Del(update_deleted_order)

    @allure.story("删除订单")
    def test_order_del(self, get_order_del_data, get_headers_h5, get_url, api_http, my_assert):
        """
        已完成和已取消的订单进行假删除
        :param get_order_del_data: 请求数据
        :param get_headers_h5:  请求头 定义参数格式和携带token
        :param get_url:  请求url 确定test/pro环境
        :param api_http: 发送get/post请求
        :param my_assert:  断言
        :return:
        """
        url = get_url(yml_data['orderDel']['path'])
        headers = get_headers_h5(type=yml_data['orderDel']['content_type'])
        method = yml_data['orderDel']['http_method']
        except_result = get_order_del_data.pop("except_result")
        response = api_http(method, url, headers, get_order_del_data)
        my_assert(response, except_result)
