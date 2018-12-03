# -*- coding: utf-8 -*-
import sqlite3
import xlrd
from sklearn.cluster import KMeans
from Tkinter import *
import math

def save2sql():
    '''
    :return: save xlsx file to database
    '''
    conn = sqlite3.connect('weibo_pois.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pois_sh_2014 (poiid TEXT, title TEXT, address, lon FLOAT, lat FLOAT, city INTEGER,
                   category TEXT, checkin_num INTEGER, photo_num INTEGER,  PRIMARY KEY (poiid))''')
    workbook = xlrd.open_workbook('poi_sh_2014.xlsx')
    sheet = workbook.sheet_by_index(0)
    for row in range(1, 283822):
        poi = []
        for col in range(0, 9):
            poi.append(sheet.cell_value(row, col))
        row += 1
        try:
            cur.execute('INSERT INTO pois_sh_2014  VALUES (?, ?, ?, ?, ? ,?, ?, ?, ?)',
                        poi)
        except:
            pass
    conn.commit()
    cur.close()

MERGE_DICT = {
    '食物': ('菜', '餐', '食', '料理'),
    '商业': ('公司', '企业', '市场', '商'),
    '教育': ('学', '校'),
    '运动': ('球场', '球馆', '体育馆', '溜冰场'),
    '医院': (u'医'),
    '交通': (u'站'),
    '居住': (u'宾馆', u'酒店')
}

def category_merge():
    '''
    :return: merge some sub-category into one category
    origin categories: 257
    '''
    conn = sqlite3.connect('weibo_pois.sqlite')
    cur = conn.cursor()
    cur.execute('''select category, count(*) from pois_sh_2014 group by category''')
    result = cur.fetchall()
    cate_dict = {}
    for r in result:
        record = False
        for key in MERGE_DICT.keys():
            if match(r[0], MERGE_DICT[key]):
                cate_dict[key] = cate_dict.get(key, 0) + r[1]
                record = True
                break
        if not record:
            cate_dict[r[0]] = int(r[1])
    cur.close()
    conn.close()
    # for key, value in cate_dict.items():
    #     print key, value
    # print '数量：', len(cate_dict)
    # print '签到：', sum(cate_dict.values())
    return cate_dict.keys()

def substitute_category():
    '''
    :return:
    '''
    # cut blocks
    category_list = category_merge()
    lat_baseline = 31.11
    lon_baseline = 121.36
    block_num = 300
    lat_interval = 0.001
    lon_interval = 0.001
    block_dict = {}

    # initiate attributes
    for i in range(0, block_num * block_num):
        block_dict[i] = [0 for _ in range(0, len(category_list))]
    conn = sqlite3.connect('weibo_pois.sqlite')
    cur = conn.cursor()
    cur.execute('''select lon, lat, category, checkin_num from pois_sh_2014''')
    result = cur.fetchall()
    # add attributes
    for r in result:
        # skip if position is out of range
        if r[0] < lon_baseline or r[0] >= lon_baseline + block_num * lon_interval \
                or r[1] < lat_baseline or r[1] >= lat_baseline + block_num * lat_interval:
            # print r
            continue
        # calculate block position number

        block_key = int((r[1] - lat_baseline) / lat_interval) * block_num +\
                int((r[0] - lon_baseline) / lon_interval)

        record = False
        for key in MERGE_DICT.keys():
            # change the category if in MERGE_DICT
            if match(r[2], MERGE_DICT[key]):
                block_dict[block_key][category_list.index(key)] += r[3]
                record = True
                break
        # keep the category if not in MERGE_DICT
        if not record:
            block_dict[block_key][category_list.index(r[2])] += r[3]
    # for key, value in block_dict.items():
    #     print key, value
    return block_dict.values()


def match(category, similar_words):
    '''
    :param category: string
    :param similar_words: tuple
    :return: if category contains any word in tuple similar_words, return True
             else return False
    '''
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    for word in similar_words:
        # print category, word
        if word in category:
            return True
    return False

def kmeans():
    # lda_results
    clf = KMeans(n_clusters=5, max_iter= 1000)
    s = clf.fit(substitute_category())

    # result
    # print s
    # print clf.cluster_centers_
    return clf.labels_

def drawboard(canvas, board, colors, startx=50, starty=50, cellwidth=50):
    width = 2 * startx + len(board) * cellwidth
    height=2 * starty + len(board) * cellwidth
    canvas.config(width=width, height=height)
    for i in range(len(board)):
        for j in range(len(board)):
            index = board[i][j]
            color = colors[index]
            cellx = startx + i * cellwidth
            celly = starty + j * cellwidth
            canvas.create_rectangle(cellx, celly, cellx + cellwidth, celly + cellwidth,
                fill = color, outline = "black")
    canvas.update()

def display():
    root = Tk()
    canvas = Canvas(root, bg="white")
    canvas.pack()
    blocks = kmeans()
    width = int(math.sqrt(len(blocks)))
    board = [blocks[i: i + width] for i in range(0, len(blocks), width)]
    # print board
    colors = ['white', 'orange', 'yellow', 'green', 'blue', 'pink']
    drawboard(canvas, board, colors, cellwidth=4)
    root.mainloop()

# save2sql()
for c in category_merge():
    print c
# substitute_category()
# display()