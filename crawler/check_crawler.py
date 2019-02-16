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

class CheckCrawler:
    def __init__(self):
        form_data = {
            'websitId': 1000001,
            'type': 3,
            'result': '',
            'checkYear': '',
            'orgName': '',
            'title': '',
            'registrationDeptCode': 1000001,
        }
        req = requests.post('http://www.chinanpo.gov.cn/search/njindex.html', data=form_data)
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

        print '共有年检结果 ：' + str(self.total_count) + '条'
        print '总页数 ：' + str(self.total_page) + '页'
        self.check_list = []

    def print_check_list(self):
        for check in self.check_list:
            print check['name'], check['department'], check['conclusion'], check['year']

    def get_check(self):
        wm = WorkManager(thread_num)
        for index in range(0, self.total_page):
            wm.add_job(index, self.get_check_by_page, index + 1)
        wm.start()
        wm.wait_for_complete()
        self.print_check_list()
        self.sort()
        return self.check_list

    def get_check_by_page(self, page):
        form_data = {
            'managerDeptCode': '',
            'result': '',
            'registrationNo': '',
            'type': 3,
            'times': '',
            'checkYear': '',
            'orgName': '',
            'registrationDeptCode': 1000001,
            'pagesize_key': 'result',
            'to_page': page,
            'page_flag': True,
            'goto_page': page,
            'current_page': 1,
            'total_count': self.total_count
        }
        req = requests.post('http://www.chinanpo.gov.cn/search/njindex.html', data=form_data)
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
            check = {
                'name': name,
                'department': level,
                'conclusion': expiry_period,
                'year': evaluate_date
            }
            self.check_list.append(check)


    def sort(self):
        self.check_list.sort(cmp=self.cmp)

    def cmp(self, temp1, temp2):
        if (temp1['year'] < temp2['year']):
            return 1
        elif (temp1['year'] == temp2['year']):
            if (temp1['conclusion'] < temp2['conclusion']):
                return 1
            elif (temp1['conclusion'] == temp2['conclusion']):
                return 0
            else:
                return -1
        else:
            return -1

    def export(self):
        export = Export()
        sheet_name = '基金会年检结论'
        items = ['名称', '业务主管单位', '年检结论', '年度']
        indexes = ['name', 'department', 'conclusion', 'year']
        export.add_sheet(sheet_name, items, indexes, self.check_list)
        export.save('基金会年检结论')



if __name__ == '__main__':
    c = CheckCrawler()
    c.get_check()
    c.export()