import csv
import os
import math
import numpy as np

'''
处理从摩拜接口爬取的原始数据，提取所有上车点并写入csv文件
'''

# 坐标类，记录了每辆车在一天内每五分钟坐标的变化
class Coordinate:
    def __init__(self):
        self.longitude = np.zeros(2016)  #经度
        self.latitude = np.zeros(2016)   #纬度

    def set(self, lon, lat, n):
        self.longitude[n] = lon
        self.latitude[n] = lat

    def get(self, n):
        return np.array((self.longitude[n], self.latitude[n]))

    def show(self):
        for i in range(2016):
            print(i, self.longitude[i], self.latitude[i])


# 创建一天内，每辆车的id与坐标变化表之间的key-value映射
def get_dict(dir_path):
    Dict = dict()
    i = 0
    for dir_name in os.listdir(dir_path):
        file_path = dir_path + dir_name + '\\'
        for file_name in os.listdir(file_path):
            file = file_path + file_name
            f = open(file, 'r')
            reader = csv.reader(f)
            for line in reader:
                if line[1] not in Dict:
                    Dict[line[1]] = Coordinate()
                    Dict[line[1]].set(line[3], line[4], i)
                else:
                    if (Dict[line[1]].get(i) == [0, 0]).all():
                        Dict[line[1]].set(line[3], line[4], i)
            i = i + 1
            f.close()
    return Dict


# 判断两点之间的距离是否足够短，依次排除部分点
def distance_is_near(x, y):
    if math.fabs(x[0] - y[0]) < 0.003 and math.fabs(x[1] - y[1]) < 0.003:
        return True
    else:
        return False


# 根据一定规则，计算聚类点
def get_all_points(path):
    dic = get_dict(path)
    print('建立映射')
    points = []
    for item in dic:
        pre_point = np.array([0, 0])
        for i in range(2016):
            if (dic[item].get(i) != [0, 0]).any():
                if (pre_point == [0, 0]).all():
                    pre_point = dic[item].get(i)
                else:
                    later_point = dic[item].get(i)
                    if (pre_point != later_point).any():
                        if distance_is_near(pre_point, later_point) == False:
                            points.append(pre_point)
                        pre_point = later_point.copy()
    print('获得聚类点')
    return np.array(points)


# 将聚类点写入csv
def write_to_csv(path, points):
    f = open(path, 'w', newline = '')
    writer = csv.writer(f)
    for i in range(len(points)):
        writer.writerow(points[i])
    f.close()
    print('写入文件')


def do():
    read_path = 'D:\\DataSet\\mobike\\Raw_data\\'
    write_path  = 'D:\\DataSet\\mobike\\Points\\points_0.003.csv'

    points = get_all_points(read_path)
    write_to_csv(write_path, points)
