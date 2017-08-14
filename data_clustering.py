import csv
import numpy as np
import model.DBSCAN as md
import matplotlib.pyplot as plt


# 将聚类点画成散点图
def show_pre_points(points, name = 'pre_points'):
    plt.figure()
    plt.title(name)
    plt.subplot(111)
    plt.plot(points[:, 0], points[:, 1], 'o')
    plt.show()


# 画聚类后的散点图
def show_after_points(points, c, name = 'result'):
    markers = ['bo', 'co', 'go', 'ko', 'mo', 'ro', 'wo', 'yo']
    plt.figure()
    plt.title(name)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.subplot(111)
    for i in range(len(c)):
        if c[i] == -1:
            continue
        j = c[i] % 8
        plt.plot(points[i, 0], points[i, 1], markers[j])
    plt.show()


# 从csv读取所有聚类点，并分块
def get_all_points_from_csv(path):
    left = 121.411
    top = 31.247

    right = 121.497
    bottom = 31.190

    lon = (right - left) / 10  # 经度差
    lat = (top - bottom) / 8  # 纬度差

    f = open(path, 'r')
    reader = csv.reader(f)
    m = []

    for i in range(80):
        l = []
        m.append(l)

    for i in reader:
        b = np.array([float(i[0]), float(i[1])])
        i = int((b[1] - bottom) / lat)
        if i >= 8:
            i = 7
        j = int((b[0] - left) / lon)
        if j >= 10:
            j = 9
        n = i * 10 + j
        m[n].append(b)

    for i in range(80):
        m[i] = np.array(m[i])
    return m


# 将聚类点和类写入csv
def write_to_csv(points, c, name, path):
    n = len(c)
    c = np.array(c)
    c = c.reshape((n, 1))

    path1 = path + name + '.csv'
    path2 = path + name + '_class.csv'
    f1 = open(path1, 'w', newline='')
    f2 = open(path2, 'w', newline='')
    writer1 = csv.writer(f1)
    writer2 = csv.writer(f2)

    for i in range(n):
        writer1.writerow(points[i])
        writer2.writerow(c[i])

    f1.close()
    f2.close()


def do():
    read_path = 'D:\\DataSet\\mobike\\Points\\points_0.003.csv'
    write_path = 'D:\\DataSet\\mobike\\Results\\'
    m = get_all_points_from_csv(read_path)
    n = len(m)
    print(n)

    eps = 0.0005
    min_points = 400

    for i in range(n):
        print('i =', i)
        name = 'result_' + str(i)
        points = m[i]

        c = md.dbscan(points, eps, min_points)
        print(name, ' 聚类完毕')

        write_to_csv(points, c, name, write_path)
        print(name, ' 写入完毕')