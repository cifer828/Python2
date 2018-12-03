# -*- coding: utf-8 -*-
import xlrd
import xlwt
import random

def shuffle_xlsx(filename):
    # 读取
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)
    all_choices = []
    # 读取单元格内容
    for row in range(0, 7306):
        choices = []
        for col in range(1, 4):
            choices.append(sheet.cell_value(row, col))
        # 选项乱序
        question = sheet.cell_value(row, 0)     # 题目
        ans = choices[0]    # 正确答案
        random.shuffle(choices)
        choices = [question] + choices + [ans]
        all_choices.append(choices)
    # 写入
    new_wb = xlwt.Workbook()
    new_sheet = new_wb.add_sheet('shuffled', cell_overwrite_ok=True)
    for row in range(0, 7306):
        for col in range(0, 5):
            new_sheet.write(row, col, all_choices[row][col])
    new_wb.save(filename[:-5] + '_shuffled' + '.xls')

shuffle_xlsx('questions.xls')


