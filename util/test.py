# -*- coding: UTF-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import csv

with open('/Users/ciel/Downloads/test.csv', 'r') as file:
    data = list(csv.reader(file))


writer_data = []
for i, val in enumerate(data):
    if i < 2:
        continue
    for j in val:
        if j.startswith('['):
            temp = []
            json_data = json.loads(j)
            for item in json_data:
                temp.append(unicode(item['donor']))
                temp.append(unicode(item['use']))
                temp.append(item['cash'])
                temp.append(item['non_cash'])
            writer_data.append(temp)



with open('result.csv', 'w') as f:
    writer = csv.writer(f)
    for row in writer_data:
        writer.writerow(row)
