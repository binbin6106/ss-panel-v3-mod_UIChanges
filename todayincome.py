import pymysql
import time
import requests
import datetime
import decimal

mysqlinfo = {'host': 'binbinss.pro', 'user': 'root', 'passwd': 'ZhfsjtJHfiZhRsYB', 'database': 'sspanel'}
filepath = 'idfile.txt'
sendapi = 'https://sc.ftqq.com/SCU37292T4696a7b5cb4db8bc991944c1f13b7d485c0bb92524731.send'


class TodayIncome(object):
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    def connect_mysql(self):
        global db
        db = pymysql.connect(self.host, self.user, self.passwd, self.database, charset='utf8')
        cursor = db.cursor()
        return cursor

    def close_db(self):
        db.close()

    def funtime(self): # flag = 0:计算前一日，=1计算前一个月第一天
        now = datetime.datetime.now()
        now_month_first_day = datetime.datetime(now.year, now.month, 1)
        delta = datetime.timedelta(days=1)
        delta_1hourago = datetime.timedelta(hours=1)
        n_days = now - delta
        n_hours = now_month_first_day - delta_1hourago
        strftime_yesterday = n_days.strftime('%Y-%m-%d %H:%M:%S')
        strftime_now_month_first_day = n_hours.strftime('%Y-%m-%d %H:%M:%S')
        date_info = {'yesterday': strftime_yesterday, 'now_month_first_day': strftime_now_month_first_day}
        return date_info
    # @staticmethod
    # def write_file(path, lastid):
    #     with open(path, 'w') as f:
    #         f.write(lastid)
    #
    # @staticmethod
    # def read_file(path):
    #     with open(path, 'r') as f:
    #         lastid = f.read()
    #     return lastid

    def find_income(self, userdatetime):
        sql = "SELECT * FROM code WHERE usedatetime > '%s'" % userdatetime
        cursor = self.connect_mysql()
        cursor.execute(sql)
        return cursor.fetchall()

    def count_income(self, flag):
        if flag == 'day':
            day_income_data = self.find_income(self.funtime()['yesterday'])
            day_income_sum = decimal.Decimal(0.00)
            for item in day_income_data:
                day_income_sum += item[3]
            return str(day_income_sum)
        elif flag == 'month':
            month_income_data = self.find_income(self.funtime()['now_month_first_day'])
            month_income_sum = decimal.Decimal(0.00)
            for item in month_income_data:
                month_income_sum += item[3]
            return month_income_sum

    def send_mes_day(self):
        day_income = self.count_income('day')
        month_income = self.count_income('month')
        day = time.strftime('%d', time.localtime(time.time()))
        month = time.strftime('%m', time.localtime(time.time()))
        text = "- #### %s日收入:%s元\n- #### %s月收入:%s元\n作者：binbin6106 \n本脚本运行于家中的ArchLinux上" % (day, day_income, month, month_income)
        textmod = {'text': '收入情况', 'desp': text}
        requests.post(sendapi, params=textmod)


if __name__ == '__main__':
    todayincome = TodayIncome(mysqlinfo['host'], mysqlinfo['user'], mysqlinfo['passwd'], mysqlinfo['database'])
    todayincome.send_mes_day()
    todayincome.close_db()
