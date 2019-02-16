# -*- coding: UTF-8 -*-


import requests
import re
import base64
import json
from bs4 import BeautifulSoup
from multi_thread.multi_thread import WorkManager
from config.config import thread_num

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class ReportListCrawler:
    def __init__(self):
        self.report_list = []
        url = 'http://www.shstj.gov.cn/node1/zhuzhan/n5/n450/index.html'
        req = requests.get(url)
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text, 'lxml')
        self.total_page = int(soup.find('a',text='末页')['href'][5:-5])


    def get_report_list(self):
        wm = WorkManager(thread_num)
        for index in range(0, self.total_page):
            wm.add_job(index, self.get_report_list_by_page, index + 1)
        wm.start()
        wm.wait_for_complete()
        return self.report_list

    def get_report_list_by_page(self, page):
        page = '' if page == 0 else str(page)
        req = requests.get('http://www.shstj.gov.cn/node1/zhuzhan/n5/n450/index' + page + '.html')
        req.encoding = 'gb2312'
        soup = BeautifulSoup(req.text, 'lxml')

        list = soup.find('ul', class_='uli14 pageList').find_all('li')
        for i in range(0, len(list)):
            li = list[i]
            a = li.a

            name = a['title']
            id = a['onclick'][10:-16]

            link = 'http://xxgk.shstj.gov.cn/showInfo/detailedInfo'
            form_data = {
                'entityId' : id
            }

            req = requests.post(link, form_data)
            req.encoding = 'gb2312'
            soup = BeautifulSoup(req.text, 'lxml')
            lis = soup.find('ul', id='minContent').find_all('li')
            trs = []
            trs1 = lis[8].table.tbody.find_all('tr')
            trs2 = lis[len(lis) - 2].table.tbody.find_all('tr')
            for tr in trs1:
                trs.append(tr)
            for tr in trs2:
                trs.append(tr)

            for tr in trs:
                tds = tr.find_all('td')
                year = tds[0].get_text()
                onclick = tds[1].a['onclick']

                report = {
                    'name': name,
                    'year': year,
                    'link': self.parse_link(onclick),
                    'id': id
                }
                self.report_list.append(report)

    def parse_link(self, onclick):
        if onclick.startswith('doPostJjh2017('):
            pattern = re.compile("doPostJjh2017\('(.+)'\);")
            result = re.findall(pattern, onclick)
            id = result[0]
            return 'http://114.80.106.68/shzzwebnew/vm/view.do?id=' + id

        elif onclick.startswith('doPostJjh('):
            pattern = re.compile("doPostJjh\('(\d+)','(.+)'\);")
            result = re.findall(pattern, onclick)
            result = result[0]
            str1 = base64.b64encode(result[0])
            str2 = base64.b64encode(result[1])
            return "http://114.80.106.68/mjzz/nj/view-report!viewReport.action?o1=OC" + str2 + "&y1=YE" + str1

        elif onclick.startswith('doPost('):
            pattern = re.compile("doPost\('(\d+)','(.+)'\);")
            result = re.findall(pattern, onclick)
            result = result[0]
            str1 = base64.b64encode(result[0])
            str2 = base64.b64encode(result[1])
            return "http://114.80.106.68/mjzz/nj/publish-nj-view-web.action?o1=OC" + str2 + "&y1=YE" + str1

        else: print onclick


if __name__ == '__main__':
    report_list_crawler = ReportListCrawler()
    report_list = report_list_crawler.get_report_list()

    print len(report_list)
    with open('report_list.json', 'w') as f:
        json.dump(report_list, f)
