# -*- coding: UTF-8 -*-


import requests
import re
import json
from bs4 import BeautifulSoup
from multi_thread.multi_thread import WorkManager
from config.config import thread_num

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class ReportListCrawler:
    def __init__(self, year):
        self.year = year
        form_data = {
            'corporateType': '',
            'websitId': '',
            'orgName': '',
            'registrationNo': '',
            'propertye': year,
            'imageField2.x': '44',
            'imageField2.y': '18'
        }
        req = requests.post('http://mzj.beijing.gov.cn/wssbweb/wssb/njxxgb/publishedSearch.do?action=publishedSearch',data=form_data)
        # print req.text
        soup = BeautifulSoup(req.text, 'lxml')
        # for linebreak in soup.find_all('br'):
        #         linebreak.extract()

        total_count_input = soup.find('input', attrs = {'name': 'total_count'})
        # print total_count_input
        self.total_count = int(total_count_input['value'])

        pattern = re.compile(u'第1/(\d+)页')
        result = re.findall(pattern, soup.get_text())
        self.total_page = int(result[0])

        print '共有年度工作报告 ：' + str(self.total_count) + '条'
        print '总页数 ：' + str(self.total_page) + '页'
        self.report_list = []

    def get_report_list(self):
        wm = WorkManager(thread_num)
        for index in range(0, self.total_page):
            wm.add_job(index, self.get_report_list_by_page, index + 1)
        wm.start()
        wm.wait_for_complete()
        return self.report_list

    def get_report_list_by_page(self, page):
        form_data = {
            'propertye': self.year,
            'corporateType': '',
            'registrationNo': '',
            'orgName': '',
            'websitId': '',
            'to_page': page,
            'page_flag': True,
            'goto_page': page,
            'current_page': 1,
            'total_count': self.total_count
        }
        req = requests.post('http://mzj.beijing.gov.cn/wssbweb/wssb/njxxgb/publishedSearch.do?action=publishedSearch', data=form_data)
        # print req.text

        soup = BeautifulSoup(req.text, 'lxml')
        # for linebreak in soup.find_all('br'):
        #     linebreak.extract()

        list = soup.find('td', class_='info-mainbg').find_all('table', recursive=False)[1].find_all('table')[2].table.find_all('tr')
        for i in range(1, len(list)):
            tr = list[i]
            tds = tr.find_all('td')
            name = tds[1]['title']
            if not name.endswith('基金会'):
                continue
            unit = tds[2]['title']
            id_number = tds[3].string
            year = tds[4].string
            title_id = str(year) + str(id_number)
            link = 'http://mzj.beijing.gov.cn/wssbweb/wssb/njxxgb/' + tds[5].a['href']
            print name, unit, id_number, year, link
            report = {
                'name': name,
                'unit': unit,
                'id_number': id_number,
                'link': link,
                'year': year,
                'title_id': title_id
            }
            self.report_list.append(report)


if __name__ == '__main__':
    report_list = []
    report_list_crawler = ReportListCrawler(2015)
    report_list.extend(report_list_crawler.get_report_list())
    # report_list_crawler = ReportListCrawler(2014)
    # report_list.extend(report_list_crawler.get_report_list())

    print len(report_list)
    with open('report_list1.json', 'w') as f:
        json.dump(report_list, f)
