import pymysql
from utils.readConfig import get_mysql


class Mysql:
    def __init__(self, **kwargs):
        # 密码全数字时需转为字符串类型
        self.conn = pymysql.connect(kwargs['host'], kwargs['account'], str(kwargs['pwd']),
                                    kwargs['dbname'])
        self.cursor = self.conn.cursor()  # 获取游标

    def query_list(self, sql):
        # 执行sql
        self.cursor.execute(sql)
        # 取出游标中所有数据
        result_list = self.cursor.fetchall()
        self.conn.close()
        return result_list

    def del_data(self, sql):
        # 执行sql
        self.cursor.execute(sql)
        self.conn.commit()
        self.conn.close()


def Search(sql):
    mysql = Mysql(**get_mysql())
    result = mysql.query_list(sql)
    return result


def Del(sql):
    try:
        mysql = Mysql(**get_mysql())
        mysql.del_data(sql)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    questionContext = '++++以下说法正确的是？'
    pkQuestion = '91a4a7d0ec75412d96cd0a2bd161bb29'
    result = Search(
        " select pkQuestion FROM `tbl_sycs_question` where questionContext='{questionContext}'".format(
            questionContext=questionContext))
    print(result)
    print(len(result))
    # mysql.del_data("DELETE from tbl_sycs_question where pkQuestion='{pkQuestion}'".format(pkQuestion=pkQuestion))
    # mysql.del_data(
    #     "DELETE from tbl_sycs_question_answer where pkQuestion='{pkQuestion}'".format(pkQuestion=pkQuestion))
