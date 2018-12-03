import matplotlib.pyplot as plt
import os

def cubic_plot():
    x_list = range(1,101)
    print x_list
    y_linear = range(2,202,2)
    print y_linear
    y_cubic = [(x ** 2) * 3 * 200 / (100 ** 2) - 2 * 200 * (x ** 3) / (100 ** 3)  for x in x_list]
    print y_cubic
    plt.plot(x_list, y_linear, '-b', label = 'linear')
    plt.plot(x_list, y_cubic, '-r', label = 'cubic')
    plt.show()

def float_range(start, end, step):
    value = start
    result = []
    while value < end:
        result.append(value)
        value += step
    return result

def cubic(s, h, l):
    return round((s ** 2) * 3 * h / (l ** 2) - 2 * h * (s ** 3) / (l ** 3), 6)

def carsim_cubic(vel):
    if vel == 120:
       linear_list1 = open('processed data\\processed7240.2\\grad2-330-straight-linear.txt').read().strip().split('\n')
    elif vel ==80:
        linear_list1 = open('processed data\\processed6710\\grad2-330-straight-linear.txt').read().strip().split('\n')
    linear_list = []
    for line in linear_list1:
        linear_list.append([float(x) for x in line.split()])
    cubic_list = []
    idx = 0
    if vel == 120:
        col = 3
    elif vel == 80:
        col = 1
    while idx < len(linear_list):
        if idx == len(linear_list) - 1:
            cubic_list.append(linear_list[idx])
            break
        if linear_list[idx][1] == linear_list[idx + 1][1] and linear_list[idx][-1] == linear_list[idx + 1][-1]:
            cubic_list.append(linear_list[idx])
            mid_point = list(linear_list[idx])
            mid_point[0] = (linear_list[idx][0] + linear_list[idx + 1][0]) / 2
            cubic_list.append(mid_point)
            idx += 1
        else:
            intervel = 0
            while linear_list[idx + intervel][1] != linear_list[idx + intervel + 1][1] or linear_list[idx + intervel][-1] != linear_list[idx + intervel + 1][-1]:
                intervel += 1
            cubic_section = []
            for idx2 in range(0, int(linear_list[idx + intervel][0] - linear_list[idx][0]) / 5):
                a_cubic_point = [linear_list[idx][0] + idx2 * 5]
                for lat_idx in range(1, 2 * col + 2):
                    if lat_idx == col + 1:
                        a_cubic_point.append(0)
                        continue
                    a_cubic_point.append(linear_list[idx][lat_idx] + cubic(idx2 * 5, linear_list[idx + intervel][lat_idx] - linear_list[idx][lat_idx], linear_list[idx + intervel][0] - linear_list[idx][0]))
                cubic_section.append(a_cubic_point)
            cubic_list += cubic_section
            idx += intervel
    cubic_str = ''
    cubic_dm_str = ''
    for line in cubic_list:
        if vel == 120:
            cubic_dm_str += str(line[0]) + ' -11.25 -7.5 -3.75 0 3.75 7.5 11.25\n'
        elif vel == 80:
            cubic_dm_str += str(line[0]) + ' -3.75 0 3.75\n'
        for item in line:
            cubic_str += str(item) + ' '
        cubic_str += '\n'
    if vel == 120:
        fhand = open('processed data\\processed7240.2\\grad2-330-straight-cubic.txt', 'wb')
        fhand_dm = open('processed data\\processed7240.2\\grad2-330-straight-cubic-dm.txt', 'wb')
    elif vel == 80:
        fhand = open('processed data\\processed6710\\grad2-330-straight-cubic.txt', 'wb')
        fhand_dm = open('processed data\\processed6710\\grad2-330-straight-cubic-dm.txt', 'wb')
    fhand.write(cubic_str)
    fhand_dm.write(cubic_dm_str)
    fhand.close()
    fhand_dm.close()



# carsim_cubic(120)
# carsim_cubic(80)

def inside():
    data = open('test.txt').read()
    prr_data = []
    for line in data.split('\n'):
        if line == '':
            break
        a_point = map(lambda x: round(float(x), 4), line.split())
        if a_point[1] < 0:
            diff = a_point[1]
        else:
            diff = a_point[-1]
        for idx in range(1, len(a_point)):
            a_point[idx] -= diff
            a_point[idx] = round(a_point[idx], 4)
        prr_data.append(a_point)
    for line in prr_data:
        print line

inside()
