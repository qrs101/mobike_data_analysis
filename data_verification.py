import csv
import requests
import numpy as np


# 读取聚类点
def read_points_from_csv(path):
    f = open(path, 'r')
    reader = csv.reader(f)
    points = []
    for i in reader:
        array = np.array([float(i[0]), float(i[1])])
        points.append(array)
    points = np.array(points)
    return points


# 读取类
def read_class_from_csv(path):
    f = open(path, 'r')
    reader = csv.reader(f)
    c = []
    for i in reader:
        num = int(i[0])
        c.append(num)
    return c


# 计算类中心坐标
def cal_center(points, c, centers):
    n = len(c)
    tmp = np.zeros((30, 2))
    num = np.zeros(30)
    k = -1

    for i in range(n):
        t = c[i]
        if t == -1:
            continue
        if t > k:
            k = t

        num[t] += 1
        tmp[t] += points[i]

    k = k + 1
    for i in range(k):
        tmp[i] = tmp[i] / num[i]
        centers.append(tmp[i])


#反向地理编码
def get_address(url):
    r = requests.get(url)
    text = r.json()
    if text['status'] != 'OK':
        return None
    address0 = text['results'][0]['formatted_address']
    address1 = text['results'][1]['formatted_address']
    return [address0, address1]


def do_1():
    read_path = 'D:\\DataSet\\mobike\\Results\\result_{}'
    write_path = 'D:\\DataSet\\mobike\\Points\\centers.csv'
    centers = []

    for i in range(80):
        path1 = read_path.format(i) + '.csv'
        path2 = read_path.format(i) + '_class.csv'
        points = read_points_from_csv(path1)
        c = read_class_from_csv(path2)
        cal_center(points, c, centers)

    centers = np.array(centers)
    f = open(write_path, 'w', newline = '')
    writer = csv.writer(f)
    for i in range(centers.shape[0]):
        writer.writerow(centers[i])
    f.close()


def do_2():
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}'
    read_path = 'D:\\DataSet\\mobike\\Points\\centers.csv'
    write_path = 'D:\\DataSet\\mobike\\Points\\address.csv'
    my_api_key = 'AIzaSyBfPlgGCvfxkLRL_6dJa8bjpXThvNf4xsY'

    f1 = open(read_path, 'r')
    f2 = open(write_path, 'w', newline = '')
    reader = csv.reader(f1)
    writer = csv.writer(f2)

    for i in reader:
        lng = float(i[0])
        lat = float(i[1])
        address = get_address(url.format(lat, lng, my_api_key))
        print(address)
        writer.writerow(address)
