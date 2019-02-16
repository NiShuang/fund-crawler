# -*- coding: UTF-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


from config.config import items
import json

def tuple2dict(tuple_list):
    d = {}
    for t in tuple_list:
        d[t[1]] = t[0]
    return d


def business_tuple2dict(tuple_list):
    d = {}
    for t in tuple_list:
        d['non_limit' + t[1]] = '非限定性本年' + t[0]
        d['limit' + t[1]] = '限定性本年' + t[0]
        d['total' + t[1]] = '合计本年' + t[0]
    return d

def welfare_tuple2dict(tuple_list):
    d = {}
    for t in tuple_list:
        d['non_cash_' + t[1]] = '非现金' + t[0]
        d['cash_' + t[1]] = '现金' + t[0]
        d['total_' + t[1]] = '合计' + t[0]
    return d


def get_dict():
    d = {}
    for index in items:
        if index == 'welfare_info':
            for i in items[index]:
                d.update(welfare_tuple2dict(items[index][i]))
        elif index == 'business_info':
            for i in items[index]:
                d.update(business_tuple2dict(items[index][i]))
        else:
            for i in items[index]:
                d.update(tuple2dict(items[index][i]))

    return d

if __name__ == '__main__':
    print json.dumps(get_dict())