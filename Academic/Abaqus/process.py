import numpy as np
import matplotlib as plt
import numpy as np

LEN_X = 0.0324
ELE_DIST = np.array([[LEN_X * -2.5, LEN_X * -1.5, LEN_X * -0.5, LEN_X * 0.5, LEN_X * 1.5, LEN_X * 2.5]])
ELE_LEN_X =  np.dot(LEN_X, np.ones([1, 6]))
ELE_LEN_Y = np.array([[0.0075],[0.0148],[0.0165],[0.0201],[0.0201],[0.0164],[0.0148],[0.0075]])
ELE_AREA = np.dot(ELE_LEN_Y, ELE_LEN_X)

def ele_data(row, col, filename):
    """
    :return: row * col matrix
    """
    f = open(filename, 'r')
    data_text = f.read()
    data_row = data_text.split('\n')
    node_data = [float(ele.split()[-1]) for ele in data_row]
    ele_data = []
    for ele_num in range(0, len(node_data), 4):
        ele_cpress = 0
        for node_num in range(4):
            ele_cpress += node_data[ele_num + node_num]
        ele_data.append(ele_cpress / 4)
    data = np.array(ele_data)
    return data.reshape(row, col)

def ele_id():
    f = open('cpress-sr-0313.txt', 'r')
    data_text = f.read()
    data_row = data_text.split('\n')
    ele_id = [ele.split()[1] for ele in data_row[::4]]
    return ele_id

# print ele_id()

def cal_resist_co():
    """
    :return:  resistance coefficient
    """
    # dist_mat = np.array([3.23905e-002, 3.23668e-002, 3.17988e-002, 3.23157e-002, 3.23507e-002, 3.25044e-002])
    # ele_cpress = ele_data(8, 6, 'cpress-sr-0313.txt')
    # ele_cnormn = ele_data(8, 6, 'cnormn-sr-0313.txt')
    # ele_cpress = ele_data(8, 6, 'cpress-rf-1-0314.txt')
    ele_cpress = ele_data(8, 6, 'cpress-rf-2-0315.txt')
    ele_torque = np.multiply(np.multiply(ELE_AREA, ele_cpress), ELE_DIST)
    # ele_torque = np.multiply(ele_cnormn, ele_dist)
    h = 0.2962
    resist_co = np.sum(ele_torque) / h / 3300
    return resist_co

print cal_resist_co()