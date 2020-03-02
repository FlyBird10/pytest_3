import pytest
from FactoryData.ContactForCorpFac import get_contact


class Test_Utils:
    """
    测试过程中批量插入数据
    """

    @pytest.mark.run(order=1)
    def test_search_cus(self, api_http):
        callCenter_headers = {"content-type": "application/json;charset=UTF-8",
                              "Authorization": "Bearer c10cfbd7-99a7-446a-8078-586578db322e",
                              "pkManagerCorp": "a18984a3636b4e4186e5"}
        callCenter_url = 'http://192.168.2.253:9998/callCenter/signing/find'
        callCenter_data = {"order": 0, "serviceDep": "", "customerArea": "", "scheduledPaymentTime": [],
                           "csManager": "",
                           "customerName": "", "isOverdue": 3, "state": None, "pageNo": 0, "pageSize": 100}
        method = 'post'
        response = api_http(method, callCenter_url, callCenter_headers, callCenter_data)
        data = response.json()['data']['object']
        global customerList
        customerList = []
        for i in data:
            customerList.append(i['pkCustomer'])
        # print(customerList)

    @pytest.mark.skip
    def test_add_contacts(self, api_http):
        headers = {"content-type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer c10cfbd7-99a7-446a-8078-586578db322e",
                   "pkManagerCorp": "a18984a3636b4e4186e5"}
        url = 'http://192.168.2.253:9998/customer/addContact'
        method = 'post'
        for i in customerList:
            data = get_contact(1)[0]
            data['pkCustomer'] = i
            print(data)
            response = api_http(method, url, headers, data)
            print(response.json())

    @pytest.mark.skip
    def test_search_contact(self, api_http):
        headers = {"content-type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer c10cfbd7-99a7-446a-8078-586578db322e",
                   "pkManagerCorp": "a18984a3636b4e4186e5"}
        url = 'http://192.168.2.253:9998/callCenter/feedback/customerDetaile'
        method = 'post'
        global contact_list
        contact_list = []
        for i in customerList:
            data = {'pkCustomer': i}
            # print(data)
            response = api_http(method, url, headers, data)
            res_data = response.json()['data']

            for j in res_data:
                contact_dict = {'client': j['name'], 'cellphone': j['cellphone'], 'position': j['duty'],
                                'pkCustomer': i}
                contact_list.append(contact_dict)
            print('*' * 50)
            print(contact_list)

    @pytest.mark.skip
    def test_add_feedback(self, api_http):
        """
        批量添加回访记录
        :param api_http:
        :return:
        """
        headers = {"content-type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer c10cfbd7-99a7-446a-8078-586578db322e",
                   "pkManagerCorp": "a18984a3636b4e4186e5"}
        url = 'http://192.168.2.253:9998/callCenter/feedback/add'
        method = 'post'
        # print('*' * 50)
        # print(contact_list)
        for i in contact_list:
            print(i)
            i['manner'] = "4781221412"
            i['particulars'] = '批量插入数据'
            i['project'] = "续签确认"
            i['remark'] = ''
            i['turnover'] = False
            response = api_http(method, url, headers, i)
            print(response.json())
        print('contact_list length is ===', len(contact_list))

    def test_show_money_log(self, api_http):
        headers = {"content-type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer c10cfbd7-99a7-446a-8078-586578db322e",
                   "pkManagerCorp": "a18984a3636b4e4186e5"}
        url = 'http://192.168.2.253:9998/payment/arrivalMoneyRecord/findAllRecord'
        method = 'post'
        data = {"pkCustomer": "1bed6dadf94b4735ad75", "pageNo": 1, "pageSize": 5, "total": 0}
        response = api_http(method, url, headers, data)
        print(response.json())
