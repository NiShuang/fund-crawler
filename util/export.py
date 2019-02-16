# -*- coding: UTF-8 -*-

import xlwt
import sys


reload(sys)
sys.setdefaultencoding("utf-8")


class Export:
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf8')    #创建工作簿


    def add_sheet(self, sheet_name, items, indexes, data):
        sheet1 = self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)  # 创建sheet
        for i in range(0, len(items)):
            sheet1.write(0, i, items[i])
        row_index = 1
        for res in data:
                rows = []
                for index in indexes:
                    rows.append(self.getValue(res, index))
                for i in range(len(rows)):
                    sheet1.write(row_index, i, rows[i])
                row_index += 1

    def save(self, filename):
        self.workbook.save('/Users/ciel/Downloads/' + filename + '.xls')  # 保存文件

    def getValue(self, res, key):
        try:
            result = res[key]
        except:
            result = ''
        return result