# -*- coding: UTF-8 -*-


import requests
import re
import time
import json
from bs4 import BeautifulSoup


import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class ReportListCrawler:
    def __init__(self):
        self.ids = [1000001, 1100001,1200001,1300001,1400001,1500001,2100001,2200001,2300001,3100001,3200001,3300001,3400001,3500001,3600001,3700001,4100001,4200001,4300001,4400001,4500001,4600001,5000001,5100001,5200001,5300001,5400001,6100001,6200001,6300001,6400001,6500001]
        self.url = 'http://www.chinanpo.gov.cn/bgsindex.html'

    def get_reports(self):
        report_list = []
        for id in self.ids:
            report_list.extend(self.get_report_by_id(id))
        return report_list

    def get_report_by_id(self, id):
        data = {
            'websitId': id,
            'registrationDeptCode': id,
            'orgName': '',
            'title': ''
        }
        res = requests.post(self.url, data)
        soup = BeautifulSoup(res.text, 'lxml')
        # for linebreak in soup.find_all('br'):
        #         linebreak.extract()

        total_count_input = soup.find('input', attrs = {'name': 'total_count'})
        if total_count_input != None:
            total_count = int(total_count_input['value'])
        else:
            total_count = 0

        pattern = re.compile(u'当前第1/(\d+)页')
        result = re.findall(pattern, soup.get_text())
        if len(result) > 0:
            total_page = int(result[0])
        else:
            total_page = 0
        print str(id) + '共有年度工作报告 ：' + str(total_count) + '条'
        print '总页数 ：' + str(total_page) + '页'
        report_list = []
        for index in range(0, total_page):
            report_list.extend(self.get_report_list_by_page(index + 1, id, total_count))
        return report_list

    def get_report_list_by_page(self, page, id, total_count):
        form_data = {
            'title': '',
            'websitId': id,
            'to_page': page,
            'page_flag': True,
            'goto_page': page,
            'current_page': 1,
            'total_count': total_count
        }

        while True:
            try:
                req = requests.post('http://www.chinanpo.gov.cn/bgsindex.html', data=form_data)
                break
            except:
                time.sleep(5)
                print 'sleep 5s'


        soup = BeautifulSoup(req.text, 'lxml')
        # for linebreak in soup.find_all('br'):
        #     linebreak.extract()

        list = soup.find('table', class_='table-1').find_all('tr')
        year_pattern = re.compile('(20\d\d)')
        report_list = []
        for i in range(1, len(list)):
            tr = list[i]
            # print tr
            a = tr.find('a')
            td = tr.find_all('td')[2]
            title = a.get_text()
            year = int(re.findall(year_pattern, title)[0])
            if year < 2013:
                continue
            pattern = re.compile('javascript:toHref\((\d+),\d+\)')
            title_id = re.findall(pattern, a['href'])[0]
            pattern = re.compile('javascript:toHref\(\d+,(\d+)\)')
            diction_id = re.findall(pattern, a['href'])[0]
            publish_date = td.get_text()
            # print title_id, diction_id, title, publish_date, year
            report = {
                'title_id': title_id,
                'title': title,
                'publish_date': publish_date,
                'diction_id': diction_id,
                'year': year,
                'area_id': id
            }
            report_list.append(report)
        time.sleep(1)
        return report_list

if __name__ == '__main__':
    crawler = ReportListCrawler()
    report_list = crawler.get_reports()

    with open('report_list.json', 'w') as f:
        json.dump(report_list, f)
