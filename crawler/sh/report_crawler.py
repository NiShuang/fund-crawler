# -*- coding: UTF-8 -*-


import requests
import re
from bs4 import BeautifulSoup, Comment
from config.config import  items as item_list

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class ReportCrawler:
    def __init__(self, report):
        requests.adapters.DEFAULT_RETRIES = 5
        self.session = requests.session()
        self.session.keep_alive = False
        self.public_check_tds = []
        self.base_info = self.get_report_by_id(report)


    def start(self):
        type_list = [
            'assets_info',
            'cash_info',
            'welfare_info',
            'public_info',
            'business_info',
            'basic_info'
        ]
        data = {}
        for type in type_list:
            data[type] = self.start_by_type(type)
        return data

    def start_by_type(self, type):
        if type == 'basic_info':
            soup = BeautifulSoup(self.html, 'html5lib')
            for comment in soup(text=lambda text: isinstance(text, Comment)):
                comment.extract()
            # [s.extract() for s in soup.find_all('script')]
            [s.extract() for s in soup.find_all(name='div', class_='Noprint')]
            self.soup = soup
        self.foundation = {}
        self.foundation.update(self.base_info)
        self.extract_info(type)
        self.format()
        self.print_foudation()
        return self.foundation


    def get_report_by_id(self, report):
        link = report['link']
        req = self.session.get(link)
        html = req.text

        html = html.replace('<br>', '').replace('<br />', '').replace('<br/>', '')
        self.html = html
        parser = 'html.parser'
        soup = BeautifulSoup(html, parser)
        for comment in soup(text=lambda text: isinstance(text, Comment)):
            comment.extract()
        # [s.extract() for s in soup.find_all('script')]
        [s.extract() for s in soup.find_all(name='div', class_='Noprint')]


        self.soup = soup
        foundation = {}
        year = report['year']
        self.foundation['year'] = year

        # self.foundation['publish_date'] = ''
        foundation['foundation_id'] = report['id']
        foundation['link'] = report['link']
        foundation['foundation_name'] = report['name']
        return foundation

    def format(self):
        if self.foundation.has_key('established_time'):
            self.foundation['established_time'] = self.foundation['established_time'].replace('年', '-').replace('月', '-').replace('日', '')
        if self.foundation.has_key('project_management'):
            if '有' in self.foundation['project_management']:
                self.foundation['project_management'] = 0
            elif '无' in self.foundation['financial_management']:
                self.foundation['project_management'] = 1
        if self.foundation.has_key('financial_management'):
            if '有' in self.foundation['financial_management']:
                self.foundation['financial_management'] = 0
            elif '无' in self.foundation['financial_management']:
                self.foundation['financial_management'] = 1

    def extract_info(self, type):
        items = item_list[type]
        if type == 'cash_info':
            for item in items['td_items']:
                self.get_cash_td_value(item)
            return

        if type == 'assets_info':
            for item in items['td_items']:
                self.get_assets_td_value(item)
            return

        if type == 'basic_info':
            for item in items['td_items']:
                self.get_td_value(item)
            for item in items['check_items']:
                self.get_check_value(item)
            for item in items['match_items']:
                self.get_match_value(item)
            for item in items['input_items']:
                self.get_input_value(item)
            return

        if type == 'public_info':
            for item in items['check_items']:
                self.get_public_check_value(item)
            return

        if type == 'welfare_info':
            for item in items['td_items']:
                self.get_welfare_td_value(item)
            return

        if type == 'business_info':
            for item in items['td_items']:
                self.get_business_td_value(item)
            return

    def print_foudation(self):
        for index in self.foundation:
            print index, self.foundation[index]

    def get_td_value(self, item):
        label = item[0]
        index = item[1]
        self.foundation[index] = ''
        td = self.soup.find(re.compile('th'), text=re.compile(label))
        try:
            if index == 'secretary_general':
                self.foundation[index] = td.parent.find_next_sibling('tr').find('td').get_text(strip=True)
                return
            td = td.find_next_sibling('td')
            input = td.find('input')
            if input == None:
                self.foundation[index] = td.get_text(strip=True)
            else:
                self.foundation[index] = input['value']
        except:
            return

    def get_assets_td_value(self, item):
        label = item[0]
        index = item[1]
        self.foundation[index] = ''
        if self.foundation['year'] == '2017':
            if index == 'proxy_assets':
                td = self.soup.find_all('th', text=re.compile(label + '$'))[1]
            else:
                td = self.soup.find('th', text=re.compile(label + '$'))
        else:
            td = self.soup.find('td', text=re.compile(label + '$'))
        try:
            if self.foundation['year'] == '2017':
                td = td.find_next_sibling('th').find_next_sibling('td').find_next_sibling('td')
            else:
                td = td.find_next_sibling('td').find_next_sibling('td').find_next_sibling('td')
            span = td.span
            if span == None:
                self.foundation[index] = td.get_text(strip=True)
            else:
                self.foundation[index] = span.get_text(strip=True)
            input = td.find('input')
            if input == None:
                self.foundation[index] = td.get_text(strip=True)
            else:
                self.foundation[index] = input['value']
            # print label
            self.foundation[index] = self.foundation[index].replace(',', '')
            # print self.foundation[index]
        except:
            return

    def get_cash_td_value(self, item):
        label = item[0]
        index = item[1]
        number = 0
        if len(item) > 2:
            number = item[2]
        self.foundation[index] = ''
        try:
            td = self.soup.find_all(re.compile('th|td'), text=re.compile(label))[number]
        except:
            return
        try:
            td = td.find_next_sibling(re.compile('th|td')).find_next_sibling('td')
            input = td.find('input')
            if input == None:
                self.foundation[index] = td.get_text(strip=True)
            else:
                self.foundation[index] = input['value']
            # print label
            self.foundation[index] = self.foundation[index].replace(',', '')
            # print self.foundation[index]
        except:
            return

    def get_business_td_value(self, item):
        label = item[0]
        index = item[1]
        self.foundation['non_limit' + index] = ''
        self.foundation['limit' + index] = ''
        self.foundation['total' + index] = ''
        if self.foundation['year'] == '2017':
            tds = self.soup.find_all('th', text=re.compile(label + '$'))
            if len(tds) > 0:
                td = tds[len(tds) - 1]
            else:
                return
        else:
            tds = self.soup.find_all('td', text=re.compile(label + '$'))
            if len(tds) > 0:
                td = tds[0]
            else:
                return

        try:
            td = td.find_next_sibling(re.compile('th|td')).find_next_sibling('td').find_next_sibling('td').find_next_sibling(
                'td').find_next_sibling('td')
            input = td.find('input')
            if input == None:
                self.foundation['non_limit' + index] = td.get_text(strip=True).replace(',', '')
            else:
                self.foundation['non_limit' + index] = input['value'].replace(',', '')
            td = td.find_next_sibling('td')
            input = td.find('input')
            if input == None:
                self.foundation['limit' + index] = td.get_text(strip=True).replace(',', '')
            else:
                self.foundation['limit' + index] = input['value'].replace(',', '')
            td = td.find_next_sibling('td')
            input = td.find('input')
            if input == None:
                self.foundation['total' + index] = td.get_text(strip=True).replace(',', '')
            else:
                self.foundation['total' + index] = input['value'].replace(',', '')
        except:
            return

    def get_welfare_td_value(self, item):
        label = item[0]
        index = item[1]
        type = item[2]
        td = self.soup.find(re.compile('td|th'), text=re.compile(label + '$'))

        if type == 1:
            self.foundation['non_cash_' + index] = ''
            self.foundation['cash_' + index] = ''
            self.foundation['total_' + index] = ''
            try:
                td = td.find_next_sibling('td')
                self.foundation['cash_' + index] = td.get_text(strip=True).replace(',', '')
                td = td.find_next_sibling('td')
                self.foundation['non_cash_' + index] = td.get_text(strip=True).replace(',', '')
                td = td.find_next_sibling('td')
                self.foundation['total_' + index] = td.get_text(strip=True).replace(',', '')
            except:
                return
            return

        if type == 2:
            self.foundation[index] = {
                'total': {
                    'cash': '0',
                    'non_cash': '0',
                },
                'list': []
            }
            try:
                trs = td.parent.find_next_sibling('tr').find_next_sibling('tr').find_next_siblings('tr')
                if len(trs) < 2:
                    return
                for i in range(0, len(trs) - 1):
                    tds = trs[i].find_all('td')
                    temp = {
                        'donor': tds[0].find('textarea').get_text(strip=True),
                        'cash': tds[1].find('input')['value'].replace(',', ''),
                        'non_cash': tds[2].find('input')['value'].replace(',', ''),
                        'use': tds[3].find('textarea').get_text(strip=True),
                    }
                    self.foundation[index]['list'].append(temp)
                tds = trs[(len(trs) - 1)].find_all('td')
                self.foundation[index]['total']['cash'] = tds[1].find('input')['value'].replace(',', '')
                self.foundation[index]['total']['non_cash'] = tds[2].find('input')['value'].replace(',', '')

            except:
                return
            return

        if type == 3:
            return

    def get_check_value(self, item):
        label = item[0]
        index = item[1]
        self.foundation[index] = ''
        if index == 'project_management' or index == 'financial_management' or index == 'foundation_type':
            td = self.soup.find(re.compile('th'), text=re.compile(label))
            try:
                self.foundation[index] = td.find_next_sibling('td').get_text(strip=True)
            except:
                return
        td = self.soup.find('td', text=re.compile(label))
        try:
            img = td.find_next_sibling('td').find('img', src=re.compile('black'))
            self.foundation[index] = unicode(img.next_sibling).strip()
        except:
            return

    def get_public_check_value(self, item):
        label = item[0]
        index = item[1]
        self.foundation[index] = ''
        td = self.get_public_check_td(label)
        if td == None:
            return
        try:
            result = ''
            text = td.get_text(strip=True)
            if '是' in text:
                result = 0
            elif '否' in text:
                result = 1
            self.foundation[index] = result
        except:
            return

    def get_public_check_td(self, label):
        return self.soup.find('td', text=re.compile(label))

    def get_match_value(self, item):
        index = item[1]
        text = item[2]
        if index == 'council_number':
            text = u'本年度共召开（(\d+)）次理事会'
        self.foundation[index] = ''

        result = re.findall(re.compile(text), self.soup.get_text())
        try:
            self.foundation[index] = result[0]
        except:
            return

    def get_input_value(self, item):
        index = item[1]
        text = item[2]
        self.foundation[index] = ''
        if index == 'project_number':
            text = u'本年度共开展了（(\d+)）项公益慈善项目'
            self.foundation[index] = ''

            result = re.findall(re.compile(text), self.soup.get_text())
            try:
                self.foundation[index] = result[0]
                return
            except:
                return

        input = self.soup.find('input', attrs={'name': re.compile(text)})
        try:
            self.foundation[index] = input['value']
        except:
            return


if __name__ == '__main__':
    c = ReportCrawler('business_info')
    # c.start_by_id(
    #     {
    #         "id": "0282f2e55a3c6aa1015a5f725599175c",
    #         "link": "http://114.80.106.68/shzzwebnew/vm/view.do?id=65E292E81B8C0088E0538202730D9177",
    #         "name": "上海青浦区诚廷社区服务中心",
    #         "year": "2017"
    #     }
    # )
