# -*- coding: UTF-8 -*-



import json
import time

from crawler.crawler_util import CrawlerUtil
from util.database import MongoDB
from report_crawler import ReportCrawler
from old_report_crawler import OldReportCrawler
from multi_thread.multi_thread import WorkManager
from config.config import thread_num

import sys


reload(sys)
sys.setdefaultencoding("utf-8")

class Crawler:
    def __init__(self):
        mongo_db = MongoDB()
        self.client = mongo_db.getClient()
        self.database = self.client['found']
        self.collection = self.database['found_record']
        self.crawler = CrawlerUtil()


    def __del__(self):
        self.client.close()

    def get_report_list(self):
        return self.collection.find({'salary': None, 'year': 2017})

    def update(self, report):
        result = self.crawler.get_salary(report)
        update_query = {"_id": report['_id']}
        self.collection.update_one(update_query, { "$set": { "salary": result[0], "reform": result[1]}})



    def start(self):
        report_list = list(self.get_report_list())
        print len(report_list)
        wm = WorkManager(thread_num)
        for index, i in enumerate(report_list):
            wm.add_job(index, self.update, i)
        wm.start()
        wm.wait_for_complete()


if __name__ == '__main__':
    c = Crawler()
    c.start()
