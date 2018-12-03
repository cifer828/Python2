import re
import os
from collections import namedtuple

WORKPATH = os.getcwd()

def print_parameter(para):
    os.chdir(para)
    files = os.listdir(os.getcwd())
    lateral_track = {}
    for f in files:
        item_name = re.findall('(.*)-.*txt$', f)[0]
        lateral_track[item_name] = process(f)
    print para
    for idx in range(len(lateral_track[item_name])):
        print lateral_track[item_name][idx][0]
        print 'Situation\t\t\t\t\t\t(Parameter, Mean, Standard Deviation, Maximum, Minimum)'
        sort_temp = []
        for key, value in lateral_track.items():
            sort_temp.append([key, value])
        sort_temp.sort(key = lambda x: x[1][idx][1])
        for item in sort_temp:
            if len(re.findall('NearStraight', item[0])) != 0:
                print item[0], '\t', item[1][idx]
            else:
                print item[0], '\t\t', item[1][idx]
        print


def one_process(str_data):
    data = str_data.split()
    name = data[1]
    list_data1 = filter(lambda x: float(x[0]) < 7000, zip(data[2: : 2], data[3: : 2]))
    list_data = map(lambda x: round(float(x[1]), 6), list_data1)
    num = len(list_data)
    maximum = max(list_data)
    minimum = min(list_data)
    mean = round(sum(list_data) / num, 6)
    std_dev = 0
    for item in list_data:
        std_dev += (item - mean) ** 2
    std_dev = round((std_dev / num) ** 0.5, 6)
    return name, mean, std_dev, maximum, minimum,


def process(filename):
    post_data = []
    str_data = open(filename).read()
    doc = re.findall('(^\*.+\*)', str_data)[0]
    list_data = str_data.strip(doc).split('\n\n')
    for dataset in list_data:
        if dataset == '':
            continue
        post_data.append(one_process(dataset))
    return post_data

# print_parameter('LateralAccel')

def demo():
    files = os.listdir(WORKPATH)
    for f in files:
        os.chdir(WORKPATH)
        if os.path.isdir(f):
            print_parameter(f)
            print '---------------------------------------'

demo()