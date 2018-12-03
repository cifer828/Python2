#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
open slide using ipython notebook
"""

import os

def open_notebook(path):
    command = 'cd ' + path + '&ipython notebook'
    # process Chinese in path, windows default encoding:gbk
    gbk_com = command.decode('utf8').encode('gbk')
    print 'dir = ' + command
    os.system(gbk_com)


path = 'C:\Users\zhqch\Documents\研究生\研一\网络搜索引擎原理'

open_notebook(path)
