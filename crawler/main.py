# -*- coding: UTF-8 -*-



import json
import time
from util.database import MongoDB
from report_crawler import ReportCrawler
from old_report_crawler import OldReportCrawler
from multi_thread.multi_thread import WorkManager
from config.config import thread_num

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class Crawler:
    def __init__(self, type):
        self.type = type
        mongoDB = MongoDB()
        self.client = mongoDB.getClient()
        database = self.client['found']
        self.collection = database[type]

    def __del__(self):
        self.client.close()

    def get_report_list(self):
        file = open('report_list.json', 'r')
        report_list = json.load(file)
        file.close()
        exist_report = self.collection.distinct("title_id")
        i = 0
        while i < len(report_list):
            if report_list[i]['title_id'] in exist_report:
                del report_list[i]
                i -= 1
            i += 1
        print len(report_list)
        for report in report_list:
            print report['title'], report['year'], report['publish_date'], report['title_id']
        return report_list


    def get_report_info(self, report):
        if report['year'] < 2017:
            c = OldReportCrawler(type)
        else:
            c = ReportCrawler(type)
        c.start_by_id(report)
        self.collection.insert(c.foundation)
        time.sleep(5)

    def start(self):
        report_list = self.get_report_list()
        wm = WorkManager(thread_num)
        for index, i in enumerate(report_list):
            wm.add_job(index, self.get_report_info, i)
        wm.start()
        wm.wait_for_complete()


if __name__ == '__main__':
    type_list = [
        # 'basic_info',
        # 'assets_info',
        # 'cash_info',
        # 'welfare_info',
        'public_info',
        # 'business_info'
    ]
    for type in type_list:
        c = Crawler(type)
        c.start()
