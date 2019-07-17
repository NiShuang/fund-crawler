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
        soup = BeautifulSoup(req.text, 'html5lib')

        report_links = soup.find_all('a', text='查看详细')
        html = ''
        for index in range(0, len(report_links) - 1):
            report_link = 'http://mzj.beijing.gov.cn' + report_links[index]['href']
            req = self.session.get(report_link)
            soup = BeautifulSoup(req.text, 'html5lib')
            try:
                report_link = 'http://mzj.beijing.gov.cn/wssb/forms/' + soup.find('input', value='查看所有')['onclick'][20:-2]
            except:
                continue
            req = self.session.get(report_link)
            html += req.text
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
        foundation['year'] = year

        # self.foundation['publish_date'] = ''
        foundation['title_id'] = report['title_id']
        foundation['id_number'] = report['id_number']
        td = self.soup.find('td', class_=re.compile('label|unnamed2'), text=re.compile(u'基金会名称'))
        try:
            foundation['foundation_name'] = td.find_next_sibling('td').find('input')['value']
        except:
            foundation['foundation_name'] = ''
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
                self.ge_public_check_value(item)
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
        td = self.soup.find(re.compile('td|th'), align='middle', text=re.compile(label))
        try:
            if index == 'secretary_general':
                self.foundation[index] = self.soup.find('input', attrs={'name': re.compile('mishuchangxingming')})['value']
                return
            if index == 'country_number':
                self.foundation[index] = self.soup.find('input', attrs={'name': re.compile('GUOJIARENYUAN')})['value']
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
        td = self.soup.find('td', class_=re.compile('unnamed2|unnamed4'), text=re.compile(label + '$'))
        try:
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
            td = self.soup.find_all('td', class_=re.compile('unnamed'), text=re.compile(label))[number]
        except:
            return
        try:
            td = td.find_next_sibling('td').find_next_sibling('td')
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
        td = self.soup.find('td', class_=re.compile('font12size'), text=re.compile(label + '$'))
        self.foundation['non_limit' + index] = ''
        self.foundation['limit' + index] = ''
        self.foundation['total' + index] = ''
        try:
            td = td.find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling(
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
        td = self.soup.find('td', text=re.compile(label + '$'))

        if type == 1:
            self.foundation['non_cash_' + index] = ''
            self.foundation['cash_' + index] = ''
            self.foundation['total_' + index] = ''
            try:
                td = td.find_next_sibling('td')
                self.foundation['cash_' + index] = td.find('input')['value'].replace(',', '')
                td = td.find_next_sibling('td')
                self.foundation['non_cash_' + index] = td.find('input')['value'].replace(',', '')
                td = td.find_next_sibling('td')
                self.foundation['total_' + index] = td.find('input')['value'].replace(',', '')
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
        if index == 'project_management' or index == 'financial_management':
            text = item[2]
            result = re.findall(re.compile(text), self.html)
            try:
                self.foundation[index] = result[0]
            except:
                return
            return

        td = self.soup.find('td', text=re.compile(label))
        try:
            img = td.find_next_sibling('td').find('img', src=re.compile('black'))
            self.foundation[index] = unicode(img.next_sibling).strip()
        except:
            return

    def ge_public_check_value(self, item):
        label = item[0]
        index = item[1]
        self.foundation[index] = ''
        td = self.get_public_check_td(label)
        if td == None:
            return
        try:
            img = td.find('img', src=re.compile('slelected'))
            result = unicode(img.next_sibling).replace(' ', '')
            if '是' in result:
                result = 0
            elif '否' in result:
                result = 1
            self.foundation[index] = result
        except:
            return

    def get_public_check_td(self, label):
        def is_public_check_td(tag):
            if tag.name != 'td':
                return False
            imgs = tag.find_all('img')
            if len(imgs) == 2:
                return True
            else:
                return False

        if self.public_check_tds == []:
            self.public_check_tds = self.soup.find_all(name=is_public_check_td)
        for td in self.public_check_tds:
            text = td.get_text()
            if label in text:
                return td
        return None

    def get_match_value(self, item):
        index = item[1]
        text = item[2]
        self.foundation[index] = ''
        if self.foundation['year'] == '2015':
            if index == 'council_number':
                try:
                    input = self.soup.find('input', attrs={'name': re.compile('alltimes')})
                    self.foundation[index] = input['value']
                except:
                    return
                return

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
            text = item[3]
            result = re.findall(re.compile(text), self.html)
            try:
                self.foundation[index] = result[0]
            except:
                return
            return
        input = self.soup.find('input', attrs={'name': re.compile(text)})
        try:
            self.foundation[index] = input['value']
        except:
            return


if __name__ == '__main__':
    c = ReportCrawler('public_info')
    # c.start_by_id(
    #     {
    #         "name": "\u5317\u4eac\u5e02\u53d1\u5c55\u4fa8\u52a1\u4e8b\u4e1a\u57fa\u91d1\u4f1a",
    #         "id_number": "0010860",
    #         "title_id": "20170010860",
    #         "link": "http://mzj.beijing.gov.cn/wssbweb/wssb/njxxgb/publishedView.do?action=publishedView&id=104951&catalogpara=N02&application=mjzz&instanceid=N0218010442016",
    #         "year": "2017",
    #         "unit": "\u5317\u4eac\u5e02\u4eba\u6c11\u653f\u5e9c\u4fa8\u52a1\u529e\u516c\u5ba4"}
    # )
    # c.start_by_id({"name": "\u5317\u4eac\u5e02\u7d27\u6025\u6551\u63f4\u57fa\u91d1\u4f1a", "id_number": "0020115", "title_id": "20160020115", "link": "http://mzj.beijing.gov.cn/wssbweb/wssb/njxxgb/publishedView.do?action=publishedView&id=104041&catalogpara=N01&application=mjzz&instanceid=N0117112742001", "year": "2016", "unit": "\u5317\u4eac\u5e02\u6c11\u653f\u5c40"})
    # c.start_by_id({"name": "\u9996\u90fd\u7ecf\u6d4e\u8d38\u6613\u5927\u5b66\u6559\u80b2\u57fa\u91d1\u4f1a", "id_number": "0020269", "title_id": "20150020269", "link": "http://mzj.beijing.gov.cn/wssbweb/wssb/njxxgb/publishedView.do?action=publishedView&id=1000074863&catalogpara=N02&application=mjzz&instanceid=N0116030342001", "year": "2015", "unit": "\u5317\u4eac\u5e02\u6559\u80b2\u59d4\u5458\u4f1a"})
