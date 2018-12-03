# -*- coding: utf-8 -*-
from pyExcelerator import *
import re
import xlutils.copy
import xlrd
import random

def open_txt(file):
    try:
        data = open(file).read()
        return data
    except:
        print 'No target file.'

def process_xy(str):
    list_xy = []
    str_list = str.strip().split('\n')
    for line in str_list:
        a_point = line.split()
        if len(a_point) > 1:
           list_xy.append(a_point)
    return list_xy

def process_ela(str):
    list_ela = []
    str_list = str.strip().split('\n')
    for line in str_list:
        point = line.split()
        if len(point) > 1:
            a_point = [float(point[3])]
            a_point.append(float(point[2]) / 10)
            a_point.append(0)
            a_point.append(float(point[4]) / 10)
            list_ela.append(a_point)
    for col in range(1, 4):
        for row in range(len(list_ela)):
            if list_ela[row][col] == 999.9:
                new_row = row
                while list_ela[new_row][col] == 999.9:
                    new_row += 1
                list_ela[row][col] = round(((list_ela[new_row][col] - list_ela[row - 1][col]) /
                                            (list_ela[new_row][0] - list_ela[row - 1][0]) *
                                            (list_ela[row][0] - list_ela[row - 1][0]) +
                                            list_ela[row -1][col]), 1)
    return list_ela

def process_1(str):
    """
    process off-center data
    """
    off_center_list = [[],[],[]]
    new_str = re.sub('K', '', str)
    new_str = re.sub('\+', '', new_str )
    basenum = int(re.findall('([0-9]+)', new_str)[0])
    str_list = new_str.strip().split('\n')
    for line in str_list:
        temp = line.split()
        for i in range(len(temp) / 2):
            a_point = (round(float(temp[2 * i]) - basenum, 3), -1 * float(temp[2 * i + 1]) / 100 * 4, 0, float(temp[2 * i + 1]) / 100 * 4)
            off_center_list[i].append(a_point)
    return off_center_list[0] + off_center_list[1] + off_center_list[2]

def write_excel(filename):
    if filename == 'x-y':
        data = process_xy(open_txt(filename + '.txt'))
    elif filename == 'chaogao':
        data = process_ela(open_txt(filename + '.txt'))
    rb = xlrd.open_workbook('my1.xls')
    wb = xlutils.copy.copy(rb)
    try:
        wb.add_sheet(filename, cell_overwrite_ok=True)
        ws = wb.get_sheet(1)
    except:
        if filename == 'x-y':
            ws = wb.get_sheet(0)
        elif filename == 'chaogao':
            ws = wb.get_sheet(1)
    for i in range(len(data)):
        for j in range(len(data[0])):
            ws.write(i, j, data[i][j])
    wb.save('my1.xls')

def trees():
    rb = xlrd.open_workbook('my1.xls')
    wb = xlutils.copy.copy(rb)
    ws = wb.get_sheet(2)
    tree_list = []
    for pos in range(-100, 5200, 50):
        tree_a = (random.random() * -10 + pos, random.random() * -5 - 30)
        tree_b = (random.random() * 10 + pos, random.random() * 5 + 30)
        tree_list.append(tree_a)
        tree_list.append(tree_b)
    for i in range(len(tree_list)):
        for j in range(2):
            ws.write(i, j, tree_list[i][j])
    wb.save('my1.xls')

def demo():
    write_excel('x-y')
    write_excel('chaogao')
    trees()

demo()
