#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import re
import matplotlib
import numpy as np
import sys
import os

matplotlib.use('Agg')  #generate images without a window appear
reload(sys)
sys.setdefaultencoding('gbk')

FigNum = 0
Color_Dict = {0: 'c-', 1: 'r-', 2: 'b-', 3: '-k', 4: '-m', 5: 'y-', 6: 'g-'}
Label_Dict = {0: 'Target Path', 1: '1/550', 2: '1/500', 3: '1/400', 4: '1/330', 5: '250', 6: '200'}
Plot_Dict = {'Track': [u'侧向偏移平均值 m', u'侧向偏移最大值 m', u'侧向偏移标准差 m'],
             'Force': [u'右前轮侧向力平均值 N', u'右前轮侧向力最大值 N', u'右前轮侧向力标准差 N'],
             'Accel': [u"侧向加速度平均值 g's", u"侧向加速度最大值 g's", u"侧向加速度标准差 g's"],
             'Angle': [u'方向盘转角平均值 deg', u'方向盘转角最大值 deg', u'方向盘转角标准差 deg']}
Name_Dict = {0: '-Mean.png', 1: '-Max.png', 2: '-std.png'}

def one_process(str_data, start, end):
    """
    :param str_data: 文本数据
    :param start，end：所选择的桩号区间
    :return:  一各桩号列表  一个对应的指标列表（偏移 受力等）
    """
    data = str_data.split()
    list_data = filter(lambda x: float(x[0]) > start and float(x[0]) < end, zip(data[2: : 2], data[3: : 2]))
    # 过滤符合桩号区间的点
    #   xx xx              [[xx, xx],
    #   xx xx     -->       [xx, xx],
    #   xx xx               [xx, xx]]
    station = []
    lateral_track = []
    for point in list_data:
        station.append(float(point[0]))
        lateral_track.append(float(point[1]))
    return station, lateral_track

def LateralTrack_Plot(filename, tag, init):
    """
    :param filename: 文件名
    :param tag: 指标名称
    :param init: 车速
    绘制或保存某指标的趋势图
    """
    global FigNum
    str_data = open(filename).read()
    doc = re.findall('(^\*.+\*)', str_data)[0]
    list_data = str_data.strip(doc).strip().split('\n\n')
    if init == 120:
        idx = 1
    elif init == 80:
        idx = 2
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20) #设置汉字字体
    plt.figure(FigNum)   # 连续作图
    for dataset in list_data:
        if idx == 0:
            idx += 1
            continue
        section = one_process(dataset, 1092, 1567)
        for i in range(len(section[1])):
            section[1][i] -= 1.7
        plt.plot(section[0], section[1], Color_Dict[idx], label = Label_Dict[idx])
        plt.legend(loc='lower right')
        idx += 1
    if tag == 'Track':
        plt.ylabel(u'侧向偏移 m', fontproperties=font)
        plt.xlabel(u'路径长度 m', fontproperties=font)
    elif tag == 'Force':
        plt.ylabel(u'右前轮侧向力 N', fontproperties=font)
        plt.xlabel(u'路径长度 m', fontproperties=font)
    plt.show()
    # plt.savefig('fig\\' + str(init) +'\\pos-change\\' + tag) #保存plot
    FigNum += 1


def mean_plot(filename, ref, start1, end1, start2, end2):
    """
    :param filename: 文本文件名
    :param ref: 参考值  指标为轨迹偏移时取1.7 其他取0
    :param start、end: 提取路段的起终点（超高过渡段）
    :return: 平均值、最大值、最小值
    """
    str_data = open(filename).read()
    doc = re.findall('(^\*.+\*)', str_data)[0]
    list_data = str_data.strip(doc).strip().split('\n\n')
    statics_data = []
    for dataset in list_data:
        statics_data.append(one_process(dataset, start1, end1)[1] + one_process(dataset, start2, end2)[1])
    data_mean = []
    data_max = []
    data_std = []
    for sups in statics_data:
        avg = sum(sups) / len(sups)
        data_mean.append(abs(avg - ref))
        temp_max = max(sups)
        temp_min = min(sups)
        if abs(temp_max - ref) > abs(temp_min - ref):
            data_max.append(abs(temp_max - ref))
        else:
            data_max.append(abs(temp_min - ref))
        dev = 0
        for point in sups:
            dev += (point - 1.7) ** 2
        data_std.append(round((dev / len(sups)) ** 0.5, 6))
    return data_mean, data_max, data_std



def data_plot120(filename, tag, sel):
    """
    :param tag: 指标 如侧偏、受力等
    :param sel: 统计指标 0：最平均值 1：最大值 2：标准差
    绘制或保存指标的折线图
    """
    global FigNum
    if tag == 'Track':
        ref = 1.7
    else:
        ref = 0
    x1 = [900, 500, 400, 330, 250]
    x2 = [550, 500, 400, 330, 250]
    y1 = mean_plot(filename, ref, 208, 908, 1580, 2280)
    y2 = mean_plot(filename, ref, 2858, 3358, 3829, 4329)
    y3 = mean_plot(filename, ref, 4723, 4724, 4724, 7083)
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20)
    plt.figure(FigNum)  #连续作图
    plt.plot(x2, y2[sel], 'bs-', label = u'极限最小半径R=650m')
    plt.plot(x1, y1[sel], 'r*-', label = u'一般最小半径R=1000m')
    plt.plot(x1, y3[sel], 'y--', label = u'不设超高半径R=5500m')
    plt.legend(loc='upper right')
    plt.legend(prop={'family':'SimHei','size':15})  #中文图例
    if sel == 0:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    elif sel == 1:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    elif sel == 2:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    plt.xlabel(u'超高渐变率倒数', fontproperties=font)
    # plt.show()
    plt.savefig('fig\\120\\rate-change\\' + tag + Name_Dict[sel])
    FigNum += 1


def data_plot80(filename, tag, sel):
    global FigNum
    if tag == 'Track':
        ref = 1.7
    else:
        ref = 0
    x = [500, 400, 330, 250, 200]
    y1 = mean_plot(filename, ref, 222, 322, 507, 607)
    y2 = mean_plot(filename, ref, 1092, 1252, 1407, 1567)
    # y3 = mean_plot(filename, ref, 1709, 1959, 2188, 2438)
    y4 = mean_plot(filename, ref, 2670, 2671, 2671, 4055)
    # y5 = mean_plot(filename, ref, 4187, 4387, 4718, 4918)
    # y6 = mean_plot(filename, ref, 5143, 5593, 6055, 6505)
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20)
    plt.figure(FigNum)
    plt.plot(x, y2[sel], 'bs-', label = u'极限最小半径R=250m')
    plt.plot(x, y1[sel], 'r*-', label = u'一般最小半径R=400m')
    plt.plot(x, y4[sel], 'y--', label = u'不设超高半径R=2500m')

    # plt.plot(x, y1[sel], 'bs-', label = 'R=250m')
    # plt.plot(x, y2[sel], 'r*-', label = 'R=400m')
    # plt.plot(x, y3[sel], 'c*-', label = 'R=600m')
    # plt.plot(x, y4[sel], 'k*-', label = 'R=2500m')
    # plt.plot(x, y5[sel], 'm*-', label = 'R=800m')
    # plt.plot(x, y6[sel], 'y*-', label = 'R=1500m')
    plt.legend(loc='upper right')
    plt.legend(prop={'family':'SimHei','size':15})
    if sel == 0:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    elif sel == 1:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    elif sel == 2:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    plt.xlabel(u'超高渐变率倒数', fontproperties=font)
    # plt.show()
    plt.savefig('fig\\80\\pos-change\\' + tag + Name_Dict[sel])
    FigNum += 1

def pp(len, vel):
    if vel == 120:
        # LateralTrack_Plot(len + '\\pos-change\\LateralTrack.txt', 'Track', vel)
        # LateralTrack_Plot(len + '\\pos-change\\LateralForceR1.txt', 'Force', vel)
        for i in range(2):
            data_plot120(len + '\\rate-change\\LateralTrack.txt', 'Track', i)
            data_plot120(len + '\\rate-change\\LateralForceR1.txt', 'Force', i)
            data_plot120(len + '\\rate-change\\LateralAccel.txt', 'Accel', i)
            data_plot120(len + '\\rate-change\\WheelAngle.txt', 'Angle', i)

    elif vel == 80:
        LateralTrack_Plot(len + '\\rate-change\\LateralTrack.txt', 'Track', vel)
        LateralTrack_Plot(len + '\\rate-change\\LateralForceR1.txt', 'Force', vel)
        for i in range(2):
            data_plot80(len + '\\pos-change\\LateralTrack.txt', 'Track', i)
            data_plot80(len + '\\pos-change\\LateralForceR1.txt', 'Force', i)
            data_plot80(len + '\\pos-change\\LateralAccel.txt', 'Accel', i)
            data_plot80(len + '\\pos-change\\WheelAngle.txt', 'Angle', i)



# pp('7240', 120)

def bar_plot(tag):
    if tag == 'Track':
        name = 'LateralTrack.txt'
        ref = 1.7
        y_label = u'侧向偏移值 m'
    elif tag == 'Force':
        name = 'LateralForceR1.txt'
        ref = 0
        y_label = u'右前轮侧向受力值 N'
    data = []
    data.append(mean_plot('6710\\pos-change\\' + name, ref, 222, 322, 507, 607)[1])
    data.append(mean_plot('6710\\pos-change\\' + name, ref, 1092, 1252, 1407, 1567)[1])
    data.append(mean_plot('6710\\pos-change\\' + name, ref, 1709, 1959, 2188, 2438)[1])
    data.append(mean_plot('6710\\pos-change\\' + name, ref, 2670, 2671, 2671, 4055)[1])
    data.append(mean_plot('6710\\pos-change\\' + name, ref, 4187, 4387, 4718, 4918)[1])
    data.append(mean_plot('6710\\pos-change\\' + name, ref, 5143, 5593, 6055, 6505)[1])
    y_curve = []
    y_straight = []
    for dataset in data:
        y_curve.append(dataset[0])
        y_straight.append(dataset[1])
    x = np.arange(len(y_curve))
    idx = 0.1
    plt.bar(x, y_curve, align = 'center', alpha = 0.2, width = 0.2, label = u'靠近直线')
    plt.bar(x + idx * 2, y_straight, align = 'center', alpha = 0.8, width = 0.2, label = u'靠近曲线')
    plt.legend(loc = 'upper right', prop={'family':'SimHei','size':15})
    plt.xticks(x + idx, ('R=250m', 'R=400m', 'R=600m', 'R=2500m', 'R=800m', 'R=1500m'))
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20)
    plt.ylabel(y_label,fontproperties=font)
    plt.show()
#
# LateralTrack_Plot('7240\\pos-change\\LateralTrack.txt', 'Track', 120)

# bar_plot('Track')
# bar_plot('Force')
# print mean_plot('7240\\preview-time\\LateralTrack.txt', 1.7, 208, 907, 908, 909)[1]
# print mean_plot('7240\\preview-time\\LateralTrack.txt', 1.7, 1579, 2279, 2280, 2281)[1]
# print mean_plot('7240\\preview-time\\LateralTrack.txt', 1.7, 2857, 3357, 3358, 3359)[1]
# print mean_plot('7240\\preview-time\\LateralTrack.txt', 1.7, 3828, 4328, 4329, 4330)[1]


def LateralTrack_Plot2(filename, tag):
    """
    :param filename: 文件名
    :param tag: 指标名称
    :param init: 车速
    绘制或保存某指标的趋势图
    """
    global FigNum
    str_data = open(filename).read()
    doc = re.findall('(^\*.+\*)', str_data)[0]
    list_data = str_data.strip(doc).strip().split('\n\n')
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20) #设置汉字字体
    idx = 0
    New_Label_Dict = {0: u'左转', 1: u'右转', 2:u'外侧车道 diff=9.2m' }
    for dataset in list_data:
        # if idx == 0:
        #     diff = 1.7
        # elif idx == 1:
        #     diff = 5.45
        # elif idx == 2:
        #     diff = 9.2
        section = one_process(dataset, 0, 4300)
        print section[1]
        for num in range(len(section[1])):
            section[1][num] = abs(section[1][num] - 20)
        plt.plot(section[0], section[1], Color_Dict[idx], label = New_Label_Dict[idx])
        plt.legend(loc='upper right', prop={'family':'SimHei','size':15} )
        idx += 1
    if tag == 'Track':
        plt.ylabel(u'侧向偏移 m', fontproperties=font)
        plt.xlabel(u'路径长度 m', fontproperties=font)
    elif tag == 'Force':
        plt.ylabel(u'右前轮侧向力 N', fontproperties=font)
        plt.xlabel(u'路径长度 m', fontproperties=font)
    plt.show()

def data_plot1202(filename, tag, sel):
    """
    :param tag: 指标 如侧偏、受力等
    :param sel: 统计指标 0：最平均值 1：最大值 2：标准差
    绘制或保存指标的折线图
    """
    global FigNum
    if tag == 'Track':
        ref = 1.7
    else:
        ref = 0
    x = [5500, 3000, 2000, 1500, 1000, 650]
    y = mean_plot(filename, ref, 0, 1, 1, 4300)
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=15)
    plt.figure(FigNum)  #连续作图
    plt.plot(x, y[sel], 'bs-')
    # plt.legend(loc='upper right')
    # plt.legend(prop={'family':'SimHei','size':15})  #中文图例
    if sel == 0:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    elif sel == 1:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    elif sel == 2:
        plt.ylabel(Plot_Dict[tag][sel], fontproperties=font)
    plt.xlabel(u'圆曲线半径', fontproperties=font)
    plt.show()
    # plt.savefig('fig\\4320\\' + tag + Name_Dict[sel])
    FigNum += 1

# data_plot1202('4320\\LateralTrack.txt', 'Track', 1)
# data_plot1202('4320\\LateralForceR1.txt', 'Force', 1)
# LateralTrack_Plot2('4320\\LateralTrack120.txt', 'Track')
# LateralTrack_Plot2('4320\\LateralForce80.txt', 'Force')

def sk120():
    x = [0, 208, 908, 1580, 2280, 2860, 3360, 3830, 4330, 4723, 4724, 7083, 7084]
    y = [0, 0, -1.0/1000, -1.0/1000, 0, 0, 1.0/650, 1.0/650, 0, 0, -1.0/5500, -1.0/5500, 0]
    return x, y
# LateralTrack_Plot('6710//rate-change//LateralTrack.txt', 'Track', 80)

def sk80():
    x = [0, 222, 322, 507, 607, 1092, 1252, 1407, 1567, 1709, 1959, 2188, 2438, 2670, 2671, 4055, 4056, 4187, 4387, 4719, 4919, 5143, 5593, 6055, 6505]
    y = [0, 0, -1.0/250, -1.0/250, 0, 0, 1.0/400, 1.0/400, 0 ,0 ,-1.0/600, -1.0/600, 0 , 0, 1.0/2500, 1.0/2500, 0, 0, -1.0/800, -1.0/800, 0, 0, -1.0/1500, -1.0/1500, 0]
    return x, y

def double_y(filename, tag, vel):
    global FigNum, Label_Dict
    if vel == 80:
        idx = 2
        end = 6710
        x, y = sk80()
    elif vel == 120:
        idx = 1
        end = 7100
        x, y = sk120()
    str_data = open(filename).read()
    doc = re.findall('(^\*.+\*)', str_data)[0]
    list_data = str_data.strip(doc).strip().split('\n\n')
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=20) #设置汉字字体
    fig, ax1 = plt.subplots()
    # Label_Dict = {1: u'靠近直线 1/250', 2: u'靠近直线 1/330', 3: u'全超高过渡', 4: u'靠近曲线 1/400', 5: u'靠近曲线 1/330', 6: u'靠近曲线 1/250',}
    Label_Dict = {1: u'1/900 & 1/550', 2: u'1/500', 3:u'1/400', 4:u'1/330', 5:u'1/250'}
    for dataset in list_data:
        # if idx == 0:
        #     diff = 1.7
        # elif idx == 1:
        #     diff = 5.45
        # elif idx == 2:
        #     diff = 9.2
        section = one_process(dataset, 0, end)
        if tag == 'Track':
            for p in range(len(section[1])):
                section[1][p] -= 1.8
        ax1.plot(section[0], section[1], Color_Dict[idx], linewidth=1, label = Label_Dict[idx])
        plt.legend(loc='upper right', prop={'family':'SimHei','size':15} )
        idx += 1
    if tag == 'Track':
        ax1.set_ylabel(u'Lateral Offset(m)', fontproperties=font)
        ax1.set_xlabel(u'Station(m)', fontproperties=font)
    elif tag == 'Force':
        ax1.set_ylabel(u'右前轮侧向力 N', fontproperties=font)
        ax1.set_xlabel(u'路径长度 m', fontproperties=font)
    ax2 = ax1.twinx()

    ax2.plot(x, y, 'c--', linewidth=1, label = u'Curvature')
    ax2.legend(prop={'family':'SimHei','size':15}, loc = 'lower right')
    ax2.set_ylabel(u'Curvature', fontproperties=font)
    ax2.set_ylim([-0.008, 0.008])
    # ax1.set_ylim([-600, 600])
    ax1.set_xlim([0, end])
    plt.show()

double_y('7240\\rate-change\\LateralTrack.txt', 'Track', 120)
# double_y('7240\\rate-change\\LateralTrack.txt', 'Track', 120)
