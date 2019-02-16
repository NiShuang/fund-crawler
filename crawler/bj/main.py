# -*- coding: UTF-8 -*-



import json
import time
from util.database import MongoDB
from report_crawler import ReportCrawler
from multi_thread.multi_thread import WorkManager
from config.config import thread_num

import sys


reload(sys)
sys.setdefaultencoding("utf-8")



type = 'business_info'
area = 'bj'

mongoDB = MongoDB()
client = mongoDB.getClient()
database = client['found']
collection = database[area + '_' + type]


def get_report_list():
    with open('report_list.json', 'r') as file:
        report_list = json.load(file)
    exist_report = collection.distinct("title_id")
    i = 0
    while i < len(report_list):
        if report_list[i]['title_id'] in exist_report:
            del report_list[i]
            i -= 1
        i += 1
    print len(report_list)
    for report in report_list:
        print report['name'], report['year'], report['link']
    return report_list


def get_report_info(report):
    c = ReportCrawler(type)
    c.start_by_id(report)
    collection.insert(c.foundation)
    # time.sleep(5)



if __name__ == '__main__':
    report_list = get_report_list()
    wm = WorkManager(thread_num)
    for index, i in enumerate(report_list):
        wm.add_job(index, get_report_info, i)
    wm.start()
    wm.wait_for_complete()

