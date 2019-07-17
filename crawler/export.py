# -*- coding: UTF-8 -*-

from util.database import MongoDB
from util.util import get_dict
from util.export import Export
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")



index_dict = get_dict()

mongoDB = MongoDB()
client = mongoDB.getClient()
database = client['bj_found1']
c_names = database.collection_names()
export_file = Export()

def export_by_c(c_name):
    collection = database[c_name]
    data = collection.find()
    indexes = (dict)(data[0]).keys()
    indexes.remove('_id')
    if indexes.__contains__('big_donate'):
        new_data = []
        indexes.remove('big_donate')
        indexes.append('big_donate_cash_total')
        indexes.append('big_donate_non_cash_total')
        indexes.append('big_donate_list')
        for d in data:
            try:
                cash_total = d['big_donate']['total']['cash']
            except:
                cash_total = ''
            try:
                non_cash_total = d['big_donate']['total']['non_cash']
            except:
                non_cash_total = ''
            try:
                big_donate_list = json.dumps(d['big_donate']['list'])
            except:
                big_donate_list = ''
            d['big_donate_cash_total'] = cash_total
            d['big_donate_non_cash_total'] = non_cash_total
            d['big_donate_list'] = big_donate_list
            new_data.append(d)

        data = new_data

    items = []
    for i in indexes:
        try:
            items.append(index_dict[i])
        except:
            items.append(i)
    export_file.add_sheet(c_name, items, indexes, data)


if __name__ == '__main__':
    for c in c_names:
        export_by_c(c)
        export_file.save("fund_bj1")

