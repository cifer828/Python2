import re
import numpy as np
import matplotlib.pyplot as plt
import xlrd

def read_rpt(filename, position, columns):
    tire_textdata = open(filename).read()
    force_data = tire_textdata.split('Label   ')
    data = []
    for t in force_data:
        temp = t.split('Minimum')[0].strip('@Loc 1').strip().strip('-')
        data.append(temp)
    data.pop(0)
    pos = []
    neg = []
    for step in data:
        # print step
        rows = step.split()
        cshearfs = rows[position::columns]
        # print cshearfs
        pos_val = 0
        neg_val = 0
        for cs1 in cshearfs:
            cs1_val = float(cs1)
            if cs1_val > 0:
                pos_val += cs1_val
            else:
                neg_val += cs1_val
        pos.append(pos_val)
        neg.append(neg_val)
    return pos, neg

def explicit_bi_cshearf():
    rpt_data = read_rpt('tire_data.rpt', 2, 5)
    pos = rpt_data[0]
    neg = rpt_data[1]
    np_pos = np.array(pos)
    np_neg = np.array(neg)
    axis_x_time = np.arange(0.025, 1.025, 0.025)
    plt.plot(axis_x_time, np_pos / 3300, label = 'cshearf_plus')
    plt.plot(axis_x_time, np_neg / 3300, label = 'cshearf_minus')
    plt.legend(loc='upper right')
    plt.show()

def standard_cshearf():
    rpt_data = read_rpt('C:\\Software\\SIMULIA\Temp\\abaqus.rpt', 4, 7)
    pos = rpt_data[0]
    neg = rpt_data[1]
    print pos[-1], neg[-1]
standard_cshearf()

def plot1():
    tire_textdata = open('tire_data.rpt').read()
    total_force = re.findall('Total(.+)\s', tire_textdata)
    total_force_data = []
    for f in total_force:
        one_interval_string = f.split()[:-1]
        one_interval_data = []
        for ois in one_interval_string:
            one_interval_data.append(float(ois))
        total_force_data.append(one_interval_data)
    total_force_data = np.array(total_force_data)
    # print len(total_force_data)
    axis_x_time = np.arange(0.025, 0.025 * len(total_force_data) + 0.025 , 0.025)
    # print axis_x_time
    workbook = xlrd.open_workbook('rolling resistance.xlsx')
    sheet1 = workbook.sheet_by_index(0)

    # displacement = np.array(sheet1.col_values(1)[1:])
    # friction_dissipation = np.array(sheet1.col_values(5)[1:])
    # external_dissipation = np.array(sheet1.col_values(3)[1:])


    co_by_fd = sheet1.col_values(7)[1:]
    co_by_fd_mean = sheet1.col_values(8)[1:]
    co_by_ew = sheet1.col_values(9)[1:]
    co_by_ew_mean = sheet1.col_values(10)[1:]

    axis_x_time_2 = np.arange(0.0001, 0.0001 * len(co_by_fd) + 0.0001, 0.0001)
    # print res_co1_1

    figure_force_eq = plt.figure('By Force Balance', figsize = (16, 8))
    plt.plot(axis_x_time, total_force_data[:, 1] / 3300, label = 'x_cshearf')
    plt.plot(axis_x_time, total_force_data[:, 2] / 3300, label = 'y_cshearf')
    plt.legend(loc='lower right')
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Rolling Resistance Coefficient', fontsize=14)

    figure_energy = plt.figure('By Energy', figsize = (16, 8))
    # plt.plot(axis_x_time_2, co_by_fd , label = 'co_by_fd')
    plt.plot(axis_x_time_2, co_by_fd_mean, label = 'co_by_fd_mean')
    # plt.plot(axis_x_time_2, co_by_ew, label = 'co_by_ew')
    plt.plot(axis_x_time_2, co_by_ew_mean, label = 'co_by_ew_mean')

    plt.legend(loc='upper right')
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Rolling Resistance Coefficient', fontsize=14)
    plt.ylim([0, 0.02])
    plt.xlim([0, 1])
    plt.show()

