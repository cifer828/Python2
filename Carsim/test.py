import matplotlib.pyplot as plt

def open_txt(filename, spl):
    data = open(filename).read().split('\n')
    result = [[],[]]
    for line in data:
        if line == '':
            break
        list_line = line.split(spl)
        result[0].append(float(list_line[0]))
        result[1].append(float(list_line[1]))
    return result

def cubic_plot():
    [x1, y1] = open_txt('1.txt', ', ')
    [x2, y2] = open_txt('2.txt', ' ')
    plt.plot(x1, y1, 'b-', label = '20')
    plt.plot(x2, y2, 'r-', label = '5')
    plt.legend(loc = 'lower left')
    plt.show()

cubic_plot()