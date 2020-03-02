from utils.generator import read_yml
from utils.DBUtil import Search, Del
import pytest
import allure
import os
import time
from urllib3 import encode_multipart_formdata

root_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(root_path, "data")
yml_data = read_yml(os.path.join(data_path, "Question.yml"))


@allure.feature("试题库")
class Test_Question:

    @allure.step("执行sql获取所需参数")
    def exec_sql_get_pkQuestion(self, get_headers):
        sql = yml_data['CheckStatus']['sql']['get_not_examing_pkQuestion']
        sql2 = yml_data['CheckStatus']['sql']['get_examing_pkQuestion']
        # 获取sql所需参数
        pkCorp = get_headers()['pkmanagercorp']
        nowTime = time.strftime("%Y-%m-%d", time.localtime())
        # 执行sql 获取pkQuestion list
        list_can_del_edit = Search(sql.format(nowTime=nowTime, pkCorp=pkCorp))
        list_forbid_del_edit = Search(sql2.format(nowTime=nowTime, pkCorp=pkCorp))
        return list_can_del_edit, list_forbid_del_edit

    @allure.step('数据准备和清理')
    @pytest.fixture(params=yml_data['AddQues']['requestList'])
    def get_add_question_data(self, request):
        sql = yml_data['AddQues']['sql']
        yield request.param
        # 删除接口插入的数据
        Del(sql['del1'].format(pkQuestion=DB_result[0][0]))
        Del(sql['del2'].format(pkQuestion=DB_result[0][0]))

    @allure.story("新增试题")
    # @pytest.mark.skip
    def test_add_question(self, get_add_question_data, get_headers, get_url, api_http, my_assert):
        global DB_result
        headers = get_headers(type=yml_data['AddQues']['content_type'])
        url = get_url(yml_data['AddQues']['path'])
        method = yml_data['AddQues']['http_method']
        except_result = get_add_question_data.pop('except_result')  # 取出请求参数对应的期望结果
        # 数据类型转json
        # get_add_question_data_json = json.dumps(get_add_question_data)
        response = api_http(method, url, headers, get_add_question_data)
        my_assert(response, except_result)  # 校验响应
        questionContext = get_add_question_data['questionContext']
        # 查询数据库，校验数据是否被插入
        sql = yml_data['AddQues']['sql']['search']
        DB_result = Search(sql.format(questionContext=questionContext))
        print('DB_result:===', DB_result)
        assert len(DB_result) == 1  # 断言只插入了一条记录

    @pytest.fixture(params=yml_data['QuesList']['requestList'])
    def get_list_ques_data(self, request):
        return request.param

    @allure.story('显示试题')
    @pytest.mark.run(order=1)
    # @pytest.mark.dependency()
    def test_list_question(self, get_headers, get_url, api_http, get_list_ques_data, my_assert):
        headers = get_headers(type=yml_data['QuesList']['content_type'])
        url = get_url(yml_data['QuesList']['path'])
        method = yml_data['QuesList']['http_method']
        except_result = get_list_ques_data.pop('except_result')

        response = api_http(method, url, headers, get_list_ques_data)

        my_assert(response, except_result)
        # 取出查询参数，截取年月日
        startDate = get_list_ques_data['startDate'].split('T')[0]
        endDate = get_list_ques_data['endDate'].split('T')[0]
        obj = response.json()['data']['list']

        if len(obj) > 0:
            # pkQuestion = obj[0]['pkQuestion']  # 查询到的第一个题目
            if endDate != '' and startDate != '':  # 搜索时间不为空时校验查询结果与查询条件是否一致
                for item in obj:  # 列表为空时不会遍历
                    createtime = int(item['createDate']) / 1000  # 字符串转整型，毫秒转秒
                    createTime = time.strftime("%Y-%m-%d", time.localtime(createtime))
                    assert createTime < endDate
                    assert createTime > startDate

    @pytest.fixture(params=yml_data['CheckStatus']['requestList'])
    def get_check_status_data(self, request, get_headers):
        global list_can_del_edit
        global list_forbid_del_edit
        list_can_del_edit, list_forbid_del_edit = self.exec_sql_get_pkQuestion(get_headers)
        if request.param['pkQuestion'] == 'del_success_sql':
            request.param['pkQuestion'] = list_can_del_edit[0][0]
        elif request.param['pkQuestion'] == 'del_fail_sql':
            request.param['pkQuestion'] = list_forbid_del_edit[0][0]
        return request.param

    # @pytest.mark.skip
    @allure.story("校验能否删除试题")
    @pytest.mark.run(order=2)
    def test_check_status(self, get_check_status_data, get_headers, get_url, api_http, my_assert):
        headers = get_headers()
        url = get_url(yml_data['CheckStatus']['path'])
        method = yml_data['CheckStatus']['http_method']
        except_result = get_check_status_data.pop('except_result')
        response = api_http(method, url, headers, get_check_status_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['EditQuestion']['requestList'])
    def get_edit_question_data(self, request, get_headers):
        global list_can_del_edit
        global list_forbid_del_edit
        if request.param['pkQuestion'] == 'del_success_sql':
            request.param['pkQuestion'] = list_can_del_edit[0][0]
        elif request.param['pkQuestion'] == 'del_fail_sql':
            request.param['pkQuestion'] = list_forbid_del_edit[0][0]
        return request.param

    @allure.story("校验能否编辑试题")
    # @pytest.mark.dependency(depends=["test_list_question"])
    @pytest.mark.run(order=2)
    def test_edit_question(self, get_edit_question_data, get_headers, get_url, api_http, my_assert):
        global Question
        Question = {}
        headers = get_headers()
        url = get_url(yml_data['EditQuestion']['path'])
        method = yml_data['EditQuestion']['http_method']
        except_result = get_edit_question_data.pop("except_result")
        response = api_http(method, url, headers, get_edit_question_data)
        obj = my_assert(response, except_result)['data']
        if obj:
            Question['answerList'] = obj['answerList']
            Question['pkQuestion'] = obj['pkQuestion']
            Question['questionAnalysis'] = obj['questionAnalysis']
            Question['questionContext'] = obj['questionContext']
            Question['questionLevel'] = obj['questionLevel']
            Question['questionType'] = obj['questionType']

    @pytest.fixture(params=yml_data['EditSaveQuestion']['requestList'])
    def get_editSave_data(self, request):
        global Question
        if request.param['answerList'] is None:
            request.param['answerList'] = Question['answerList']
        if request.param['pkQuestion'] is None:
            request.param['pkQuestion'] = Question['pkQuestion']
        if request.param['questionAnalysis'] is None:
            request.param['questionAnalysis'] = Question['questionAnalysis']
        if request.param['questionContext'] is None:
            request.param['questionContext'] = '修改后' + Question['questionContext']
        if request.param['questionLevel'] is None:
            request.param['questionLevel'] = Question['questionLevel']
        if request.param['questionType'] is None:
            request.param['questionType'] = Question['questionType']
        return request.param

    # @pytest.mark.dependency(depends=["test_edit_question"])  # 用例被跳过？？
    # @pytest.mark.skip
    @pytest.mark.run(order=3)
    @allure.story("保存修改的题目")
    def test_edit_save_question(self, get_headers, get_url, get_editSave_data, api_http, my_assert):
        headers = get_headers(type=yml_data['EditSaveQuestion']['content_type'])
        url = get_url(yml_data['EditSaveQuestion']['path'])
        except_result = get_editSave_data.pop("except_result")
        method = yml_data['EditSaveQuestion']['http_method']
        # get_editSave_data_json = json.dumps(get_editSave_data)
        response = api_http(method, url, headers, get_editSave_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['DelQuestion']['requestList'])
    def get_del_data(self, request):
        global list_can_del_edit
        if request.param['pkQuestion'] == 'del_success_sql':
            request.param['pkQuestion'] = list_can_del_edit[0][0]
        return request.param

    @allure.story("删除题目")
    def test_del_question(self, get_headers, get_url, api_http, get_del_data, my_assert):
        headers = get_headers()
        url = get_url(yml_data['DelQuestion']['path'])
        method = yml_data['DelQuestion']['http_method']
        except_result = get_del_data.pop('except_result')
        response = api_http(method, url, headers, get_del_data)
        my_assert(response, except_result)

    @pytest.fixture(params=yml_data['ImportQuestion']['requestList'])
    def get_import_data(self, request):
        path = request.param['file']
        filename = os.path.basename(path)
        with open(path, 'rb') as f:
            file = {
                "file": (filename, f.read())
            }
        encode_data = encode_multipart_formdata(file)
        request.param['file'] = encode_data
        return request.param

    @allure.story("导入试题")
    # @pytest.mark.skip
    def test_import_question(self, get_headers, get_url, get_import_data, api_http, my_assert):
        headers = get_headers(type=yml_data['ImportQuestion']['content_type'], content=get_import_data['file'][1])
        url = get_url(yml_data['ImportQuestion']['path'])
        method = yml_data['ImportQuestion']['http_method']
        except_result = get_import_data.pop('except_result')
        response = api_http(method, url, headers, get_import_data['file'][0])
        my_assert(response, except_result)
