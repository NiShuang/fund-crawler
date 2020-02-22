# -*- coding: UTF-8 -*-

from util.database import MongoDB
from util.util import get_dict
from util.export import Export
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")




mongoDB = MongoDB()
client = mongoDB.getClient()
database = client['found']

collection = database['found_record']
with open('report_list.json') as my_file:
    reports = json.load(my_file)
    for report in reports:
        if report['year'] in [2015, 2017]:
            collection.insert(report)


