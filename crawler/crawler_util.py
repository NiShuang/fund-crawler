# -*- coding: UTF-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from config.config import thread_num, items as item_list

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class CrawlerUtil:
    def __init__(self):
        requests.adapters.DEFAULT_RETRIES = 5
        self.session = requests.session()
        self.session.keep_alive = False


    def get_salary(self, report):
        pattern1 = re.compile(u'专职工作人员的年平均年工资为：(.*?)元')
        pattern2 = re.compile(u'pingjunniangongzi\'  value=\'(.*?)\'  ID')
        pattern4 = re.compile(u'年度责令整改通知书.*?slelected')

        salary = None
        zhenggai = None
        html = self.get_html(report)
        # print html
        result = re.findall(pattern1, html)
        if len(result) == 0:
            result = re.findall(pattern2, html)
        if len(result) > 0:
            salary = result[len(result) - 1]

        result = re.findall(pattern4, html)
        if len(result) > 0:
            result = result[0]
            if '是' in  result:
                zhenggai = 0
            else:
                zhenggai = 1
        print (salary, zhenggai)
        return (salary, zhenggai)



    def get_html(self, report):
        form_data = {
            'id': report['title_id'],
            'websitId': report['area_id'],
            'dictionid': report['diction_id'],
            'netTypeId': 2,
            'topid': ''
        }
        text = self.session.post('http://www.chinanpo.gov.cn/viewbgs.html', data=form_data).text
        return text
