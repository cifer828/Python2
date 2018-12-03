# -*- coding: utf-8 -*-
import re
import xlrd
import random
import os

working_path = os.getcwd()
DIRNAME = '7240'
LANE_NUM = 3

def open_txt(filename):
    os.chdir(working_path + '\\raw data\\raw' + DIRNAME)
    try:
        fhand = open(filename)
        data = fhand.read()
        fhand.close()
        return data
    except:
        print 'No target file.'

def trees(lenth):
    os.chdir(working_path + '\\processed data\\processed' + DIRNAME)
    fhand = open('trees.txt', 'wb')
    tree_list = []
    tree_str = ''
    for pos in range(-100, lenth, 50):
        tree_a = (random.random() * -10 + pos, random.random() * -5 - 30)
        tree_b = (random.random() * 10 + pos, random.random() * 5 + 30)
        tree_list.append(tree_a)
        tree_list.append(tree_b)
    for tree in tree_list:
        tree_str += str(tree[0]) + ' ' + str(tree[1]) + '\n'
    fhand.write(tree_str)
    fhand.close()
    print 'trees.txt', 'Saved'

def process_xy(filename):
    data = open_txt(filename)
    os.chdir(working_path + '\\processed data\\processed' + DIRNAME)
    fhand = open(filename, 'wb')
    str_list = data.strip().split('\n')
    fhand.write('0 0\n')
    for line in str_list:
        a_point = line.split()
        if len(a_point) > 1:
            trees_len = int(float(a_point[0]))
            fhand.write(a_point[1])
            fhand.write(' ')
            fhand.write(a_point[2])
            fhand.write('\n')
    fhand.close()
    trees(trees_len + 100)
    print filename, 'Saved.'

# process_xy('x-y.txt')

def process_linear_sup(filename):
    data = open_txt(filename)
    os.chdir(working_path + '\\processed data\\processed' + DIRNAME)
    fhand = open(filename[: -4] + '-linear.txt', 'wb')
    str_list = data.strip().split('\n')
    list_sup = []
    for line in str_list:
        point = line.split()
        if len(point) > 3:
            a_point = [float(point[3])]
            for i in range(LANE_NUM, 0, -1):
                a_point.append(float(point[2]) / 100 * i * 3.75)
            a_point.append(0)
            for i in range(1, LANE_NUM + 1):
                a_point.append(float(point[4]) / 100 * i * 3.75)
            list_sup.append(a_point)
    for col in range(1, 2 * LANE_NUM + 2):
        for row in range(len(list_sup)):
            if list_sup[row][col] > 10:
                new_row = row
                while list_sup[new_row][col] > 10:
                    new_row += 1
                list_sup[row][col] = round(((list_sup[new_row][col] - list_sup[row - 1][col]) /
                                            (list_sup[new_row][0] - list_sup[row - 1][0]) *
                                            (list_sup[row][0] - list_sup[row - 1][0]) +
                                            list_sup[row -1][col]), 4)
    for line in list_sup:
        for item in line:
            fhand.write(str(item))
            fhand.write(' ')
        fhand.write('\n')
    fhand.close()
    print filename[: -4] + '-linear.txt', 'Saved'
    fhand2 = open(filename[: -4] + '-linear-dm.txt', 'wb')
    str_dm = ''
    for line in list_sup:
        if LANE_NUM == 3:
            str_dm += str(line[0]) + ' -11.25 -7.5 -3.75 0 3.75 7.5 11.25\n'
        elif LANE_NUM == 1:
            str_dm += str(line[0]) + ' -3.75 0 3.75\n'
    fhand2.write(str_dm)
    fhand2.close()
    print filename[: -4] + '-linear-dm.txt', 'Saved'

# process_linear_sup('sup-1-1.txt')
# process_linear_sup('sup-1-2.txt')

def process_cubic_sup(filename):
    os.chdir(working_path + '\\raw data\\raw' + DIRNAME)
    workbook = xlrd.open_workbook(filename)
    list_sup = []
    list_dm = []
    str_sup = ''
    idx = 0
    while True:
        sheet = workbook.sheet_by_index(idx)
        try:
            test = sheet.cell_value(0, 0)
        except:
            break
        for row in range(4, 27):
            raw_station = sheet.cell_value(row, 0)
            station1 = re.sub('K', '', raw_station)
            station = re.sub('\+', '', station1)
            left_sup = sheet.cell_value(row, 4)
            right_sup = sheet.cell_value(row, 9)
            if station == '':
                break
            a_point = [station]
            for i in range(LANE_NUM, 0, -1):
                a_point.append(round(left_sup / 100 * i * 3.75, 4))
            a_point.append(0)
            for i in range(1, LANE_NUM + 1):
                a_point.append(round(right_sup / 100 * i * 3.75, 4))
            # if len(list_sup) < 3:
            #     list_sup.append(a_point)
            # elif a_point[2: ] == list_sup[-1][2: ] and a_point[2: ] == list_sup[-2][2: ] and a_point[2: ] == list_sup[-3][2: ]:
            #     list_sup.pop()
            #     list_dm.pop()
            #     list_sup.append(a_point)
            # else:
            list_sup.append(a_point)

            if LANE_NUM == 3:
                list_dm.append(station + ' -11.25 -7.5 -3.75 0 3.75 7.5 11.25\n')
            elif LANE_NUM == 1:
                list_dm.append(station + ' -3.75 0 3.75\n')
        idx += 1
    for point in list_sup:
        for p in point:
            str_sup += str(p) + ' '
        str_sup += '\n'
    os.chdir(working_path + '\\processed data\\processed' + DIRNAME)
    fhand = open(filename[: -4] + '.txt', 'wb')
    fhand.write(str_sup)
    fhand.close()
    print filename[: -4] + '.txt', 'Saved'
    fhand2 = open(filename[: -4] + '-dm.txt', 'wb')
    for line in list_dm:
        fhand2.write(line)
    fhand2.close()
    print filename[: -4] + '-dm.txt', 'Saved'


# process_cubic_sup('sup-2-1.xls')
# process_cubic_sup('sup-2-2.xls')


def process():
    global DIRNAME, LANE_NUM
    DIRNAME = '4320'
    LANE_NUM = 3
    files = os.listdir(working_path + '\\raw data\\raw' + DIRNAME)
    for f in files:
        if f[: 3] == 'x-y':
            process_xy(f)
        elif f[-3: ] == 'txt':
            process_linear_sup(f)
        elif f[-9: ] == 'cubic.xls':
            process_cubic_sup(f)

process()