from utils.generator import read_yml
import pytest
import allure
import os
from FactoryData.ContactForCorpFac import get_subject
from test_case.test_finance.test_O0_assistAccoun import TestAssisAccoun

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")
yml_data = read_yml(os.path.join(finance_path, "finance_initbalance.yml"))
common = read_yml(os.path.join(finance_path, "common.yml"))


@allure.feature("科目及期初")
class Test_finance_initbalance:

    @pytest.fixture(params=yml_data['initialBalanceList']['requestList'])
    def get_find_init_balance_data(self, request):
        request.param['pkAccountBook'] = common['pkAccountBook']
        return request.param

    @allure.story("查询科目及期初列表")
    @pytest.mark.run(order=1)
    @allure.severity('blocker')
    def test_find_init_balance(self, get_find_init_balance_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['initialBalanceList']['content_type'])
        url = get_url(yml_data['initialBalanceList']['path'])
        method = yml_data['initialBalanceList']['http_method']
        except_result = get_find_init_balance_data.pop("except_result")
        with allure.step("调用查询科目接口"):
            response = api_http(method, url, headers, get_find_init_balance_data)
        with allure.step("断言接口响应成功"):
            global respAllInitBalance
            respAllInitBalance = my_assert(response, except_result)
            assert len(respAllInitBalance['data']) > 0  # 校验至少返回了一个科目
        with allure.step("校验父级科目余额等于其子级科目余额之和"):
            initBalanceList = respAllInitBalance['data']
            totalCreditList = []
            totalDebitList = []
            initialBalanceList = []
            yearsBalanceList = []
            # 为一级科目余额赋初始值，以便第一次循环使用
            # firstTotalCredit = 0
            # firstTotalDebit = 0
            # firstInitialBalance = 0
            # firstYearsBalance = 0
            for initBalance in initBalanceList:
                if initBalance['parentCode'] == 0:  # 一级科目
                    if len(totalCreditList) > 0:  # 存在子级时才需要校验
                        # 校验上一个科目余额是否等于其子级余额之和
                        assert firstTotalCredit == sum(totalCreditList)
                        assert firstTotalDebit == sum(totalDebitList)
                        assert firstInitialBalance == sum(initialBalanceList)
                        assert firstYearsBalance == sum(yearsBalanceList)
                    # 清空之前的子级元素
                    totalCreditList.clear()
                    totalDebitList.clear()
                    initialBalanceList.clear()
                    yearsBalanceList.clear()

                    firstTotalCredit = initBalance['totalCredit']  # 一级科目的本年累计贷方
                    firstTotalDebit = initBalance['totalDebit']  # 一级科目的本年累计借方
                    firstInitialBalance = initBalance['initialBalance']  # 一级科目的期初余额
                    firstYearsBalance = initBalance['yearsBalance']  # 一级科目的年初余额
                    firstCode = initBalance['subjectCode']  # 一级科目的科目编码

                elif initBalance['parentCode'] == firstCode:
                    totalCreditList.append(initBalance['totalCredit'])  # 将子级对应余额加入list中以便后续求和
                    totalDebitList.append(initBalance['totalDebit'])
                    initialBalanceList.append(initBalance['initialBalance'])
                    yearsBalanceList.append(initBalance['yearsBalance'])
        get_find_init_balance_data['except_result'] = except_result  # 删除的期望结果再加入dict中，以便后续使用
        # print('科目数量：', len(resp['data']))
        return respAllInitBalance

    @pytest.fixture(params=yml_data['editInitialBalance']['requestList'])
    def get_edit_init_balance_data(self, request):
        request.param['pkAccountBook'] = common['pkAccountBook']
        for initBalance in respAllInitBalance['data']:  # 遍历科目列表，替换对应科目的相关信息
            if initBalance['subjectName'] == request.param['subjectName']:
                # request.param['pkAccountBook'] = initBalance['pkAccountBook']
                request.param['pkInitialBalance'] = initBalance['pkInitialBalance']
                request.param['subjectCode'] = initBalance['subjectCode']
                request.param['subjectType'] = initBalance['subjectType']
                request.param['direction'] = initBalance['direction']
        return request.param

    @allure.story("编辑科目及期初余额")
    @pytest.mark.run(order=2)
    def test_edit_init_balance(self, get_edit_init_balance_data, get_headers, get_url, api_http, my_assert,
                               get_find_init_balance_data):
        headers = get_headers(type=yml_data['editInitialBalance']['content_type'])
        url = get_url(yml_data['editInitialBalance']['path'])
        method = yml_data['editInitialBalance']['http_method']
        except_result = get_edit_init_balance_data.pop("except_result")
        yearsBalance = except_result.pop("yearsBalance")
        print(get_edit_init_balance_data)
        response = api_http(method, url, headers, get_edit_init_balance_data)
        get_edit_init_balance_data['except_result'] = except_result
        my_assert(response, except_result)
        with allure.step("调用查询接口校验余额是否修改成功"):
            # 查询接口 校验数据被修改成功
            initBalanceList = \
                self.test_find_init_balance(get_find_init_balance_data, get_headers, get_url, api_http, my_assert)[
                    'data']
            for initBalance in initBalanceList:
                if initBalance['subjectCode'] == get_edit_init_balance_data['subjectCode']:
                    assert initBalance['initialBalance'] == get_edit_init_balance_data['initialBalance']
                    assert initBalance['totalCredit'] == get_edit_init_balance_data['totalCredit']
                    assert initBalance['totalDebit'] == get_edit_init_balance_data['totalDebit']
                    assert initBalance['yearsBalance'] == yearsBalance

    @pytest.fixture(params=yml_data['addSubject']['requestList'])
    def get_add_subject_data(self, request):
        # request.param['subjectName'] = get_subject()[0]['subjectName']  # 科目名称随机生成
        request.param['subjectName'] = '测试C'
        request.param['pkAccountBook'] = common['pkAccountBook']
        return request.param

    @allure.story("添加科目")
    # @pytest.mark.skip
    def test_add_subject(self, get_add_subject_data, get_headers, get_url, api_http, my_assert,
                         get_find_init_balance_data):
        with allure.step("查询父级已有子级数"):
            initBalanceList = \
                self.test_find_init_balance(get_find_init_balance_data, get_headers, get_url, api_http, my_assert)[
                    'data']
            child = 0  # 子级数
            subNum = len(initBalanceList)  # 科目数
            for initBalance in initBalanceList:
                if initBalance['parentCode'] == get_add_subject_data['parentCode']:
                    child += 1
            if 0 < child < 10:
                childCode = str(get_add_subject_data['parentCode']) + '0' + str(child)
            elif child >= 10:
                childCode = str(get_add_subject_data['parentCode']) + str(child)
            elif child == 0:
                childCode = str(get_add_subject_data['parentCode']) + '00'
            childCode = int(childCode)
        headers = get_headers(type=yml_data['addSubject']['content_type'])
        url = get_url(yml_data['addSubject']['path'])
        method = yml_data['addSubject']['http_method']
        except_result = get_add_subject_data.pop("except_result")
        with allure.step("调用新增接口，校验新增的科目编码是否正确"):
            response = api_http(method, url, headers, get_add_subject_data)
            resp = my_assert(response, except_result)['data']
            assert resp['subjectCode'] == childCode + 1
        get_add_subject_data['except_result'] = except_result
        with allure.step("查询科目数是否增加"):
            initBalanceListNew = \
                self.test_find_init_balance(get_find_init_balance_data, get_headers, get_url, api_http, my_assert)[
                    'data']
            assert len(initBalanceListNew) == subNum + 1

    @pytest.fixture(params=yml_data['opt']['requestList'])
    def get_opt_data(self, request):
        request.param['pkAccountBook'] = common['pkAccountBook']
        return request.param

    @allure.story("查询辅助列表")
    def test_opt(self, get_opt_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers(type=yml_data['opt']['content_type'])
        url = get_url(yml_data['opt']['path'])
        method = yml_data['opt']['http_method']
        except_result = get_opt_data.pop("except_result")
        response = api_http(method, url, headers, get_opt_data)
        global optList
        optList = my_assert(response, except_result)
        # return optList

    @pytest.fixture(params=yml_data['setWL']['requestList'])
    def get_set_WL_data(self, request, get_headers, get_url, api_http, my_assert,
                        get_find_all_contacts_data, get_find_init_balance_data):
        # respAllInitBalance = self.test_find_init_balance(get_find_init_balance_data, get_headers, get_url, api_http,
        #                                                  my_assert)
        # request.param['pkAccountBook'] = respAllInitBalance['data'][0]['pkAccountBook']
        request.param['pkAccountBook'] = common['pkAccountBook']
        # TODO (heli)： 数据准备，添加客户
        print('设置往来的数据准备')
        yield request.param
        print('设置往来的数据清理')

    @allure.story("设置往来")
    def test_setWL(self, get_set_WL_data, get_headers, get_url, api_http, my_assert, get_find_init_balance_data,
                   test_find_all_contacts, get_find_all_contacts_data):
        with allure.step("新增客户并查询其PK"):
            # TestAssisAccoun().test_add_contacts(get_add_contacts_data, get_headers, get_url, api_http, my_assert)
            # projectList = TestAssisAccoun().test_find_all_contacts(get_find_all_contacts_data, get_headers, get_url,
            #                                                        api_http,
            #                                                        my_assert)
            contactList = test_find_all_contacts(get_find_all_contacts_data, get_headers, get_url, api_http, my_assert)
            # 设置该科目的往来客户为列表中的第一个客户
            get_set_WL_data['pkContacts'] = contactList[0]['pkContacts']  # 设置客户主键
        print('pkContacts:====', get_set_WL_data['pkContacts'])
        with allure.step("查询科目是否有余额"):
            AllInitBalancelist = respAllInitBalance['data']
            for AllInitBalance in AllInitBalancelist:
                if AllInitBalance['subjectCode'] == get_set_WL_data['subjectCode']:
                    get_set_WL_data['pkInitialBalance'] = AllInitBalance['pkInitialBalance']
        print('pkInitialBalance:====', get_set_WL_data['pkInitialBalance'])
        headers = get_headers(type=yml_data['setWL']['content_type'])
        url = get_url(yml_data['setWL']['path'])
        method = yml_data['setWL']['http_method']
        except_result = get_set_WL_data.pop("except_result")
        response = api_http(method, url, headers, get_set_WL_data)
        resp = my_assert(response, except_result)
        get_set_WL_data['except_result'] = except_result
        print(resp)
        # assert 0
