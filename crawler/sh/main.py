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
area = 'sh'
# 修复sh basic assets 的name
mongoDB = MongoDB()
client = mongoDB.getClient()
database = client['found']
collection = database[area + '_' + 'found_record']

# def fix_name(report):
#     print report['name'], report['year'], report['link']
#     collection.update({'link':report['link']},{'$set':{'foundation_name':report['name']}})

def get_all_report():
    with open('report_list.json', 'r') as file:
        report_list = json.load(file)
    return report_list

def get_report_list():
    with open('report_list.json', 'r') as file:
        report_list = json.load(file)

    exist_report = collection.distinct("link")
    i = 0
    while i < len(report_list):
        if report_list[i]['link'] in exist_report:
            del report_list[i]
            i -= 1
        i += 1
    print len(report_list)
    for report in report_list:
        print report['name'], report['year'], report['link']
    return report_list


def get_report_info(report):
    c = ReportCrawler(report)
    data = c.start()
    type_list = [
        'basic_info',
        'assets_info',
        'cash_info',
        'welfare_info',
        'public_info',
        'business_info'
    ]
    for type in type_list:
        database[area + '_' + type].insert(data[type])
    collection.insert(report)
    # time.sleep(5)



if __name__ == '__main__':
    report_list = get_report_list()
    wm = WorkManager(thread_num)
    for index, i in enumerate(report_list):
        wm.add_job(index, get_report_info, i)
    wm.start()
    wm.wait_for_complete()

    # report_list = get_all_report()
    # wm = WorkManager(thread_num)
    # for index, i in enumerate(report_list):
    #     wm.add_job(index, fix_name, i)
    # wm.start()
    # wm.wait_for_complete()


