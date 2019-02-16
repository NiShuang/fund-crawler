# -*- coding: UTF-8 -*-


import requests
import re
from bs4 import BeautifulSoup
from util.export import Export
from multi_thread.multi_thread import WorkManager
from config.config import thread_num

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class EvaluationCrawler:
    def __init__(self):
        req = requests.get('http://www.chinanpo.gov.cn/search/evaltindex.html')
        # print req.text

        soup = BeautifulSoup(req.text, 'lxml')
        # for linebreak in soup.find_all('br'):
        #         linebreak.extract()

        total_count_input = soup.find('input', attrs = {'name': 'total_count'})
        # print total_count_input
        self.total_count = int(total_count_input['value'])

        pattern = re.compile(u'当前第1/(\d+)页')
        result = re.findall(pattern, soup.get_text())
        self.total_page = int(result[0])

        print '共有评估结果 ：' + str(self.total_count) + '条'
        print '总页数 ：' + str(self.total_page) + '页'
        self.evaluation_list = []

    def print_evaluation_list(self):
        for evaluation in self.evaluation_list:
            print evaluation['name'], evaluation['level'], evaluation['expiry_period'], evaluation['evaluate_date']

    def get_evaluation(self):
        wm = WorkManager(thread_num)
        for index in range(0, self.total_page):
            wm.add_job(index, self.get_evaluation_by_page, index + 1)
        wm.start()
        wm.wait_for_complete()
        self.print_evaluation_list()
        self.sort()
        self.filter()
        return self.evaluation_list

    def get_evaluation_by_page(self, page):
        form_data = {
            'orgName': '',
            'evalYear': '',
            'evalLevel': '',
            'evalDateStart': '',
            'evalDateEnd': '',
            'relationId': '',
            'orgId': '',
            'registrationDeptCode': '',
            'pagesize_key': 'EvaluateResultInfo',
            'to_page': page,
            'page_flag': True,
            'goto_page': page,
            'current_page': 1,
            'total_count': self.total_count
        }
        req = requests.post('http://www.chinanpo.gov.cn/search/evaltindex.html', data=form_data)
        # print req.text

        soup = BeautifulSoup(req.text, 'lxml')
        # for linebreak in soup.find_all('br'):
        #     linebreak.extract()

        list = soup.find('table', class_='table-1').find_all('tr')
        for i in range(1, len(list)):
            tr = list[i]
            # print tr
            td_list = tr.find_all('td')
            name = td_list[1].get_text()
            level = td_list[2].get_text()
            expiry_period = td_list[3].get_text(strip=True).replace('\t','').replace('\r','').replace('\n','')
            evaluate_date = td_list[4].get_text()
            # print name, level, expiry_period, evaluate_date
            evaluation = {
                'name': name,
                'level': level,
                'expiry_period': expiry_period,
                'evaluate_date': evaluate_date
            }
            self.evaluation_list.append(evaluation)

    def filter(self):
        i = 0
        while i < len(self.evaluation_list):
            name = self.evaluation_list[i]['name']
            if (not name.endswith('基金会')):
                del self.evaluation_list[i]
                i -= 1
            i += 1


    def sort(self):
        self.evaluation_list.sort(cmp=self.cmp)

    def cmp(self, temp1, temp2):
        if (temp1['evaluate_date'] < temp2['evaluate_date']):
            return 1
        elif (temp1['evaluate_date'] == temp2['evaluate_date']):
            if (temp1['expiry_period'] < temp2['expiry_period']):
                return 1
            elif (temp1['expiry_period'] == temp2['expiry_period']):
                return 0
            else:
                return -1
        else:
            return -1

    def export(self):
        export = Export()
        sheet_name = '基金会评估信息'
        items = ['名称', '评估等级', '等级有效期', '评估时间']
        indexes = ['name', 'level', 'expiry_period', 'evaluate_date']
        export.add_sheet(sheet_name, items, indexes, self.evaluation_list)
        export.save('基金会评估信息')



if __name__ == '__main__':
    c = EvaluationCrawler()
    c.get_evaluation()
    c.export()