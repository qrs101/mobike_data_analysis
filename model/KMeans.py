import math
import numpy as np

#距离平方
def distance(p, q):
    return np.power(p - q, 2).sum()

#计算中心点
def cal_center(m, classifications, k):
    new_centers = np.zeros((k, 2))
    cluster_points = np.zeros(k)
    num_points = m.shape[0]
    for i in range(num_points):
        cluster_id = classifications[i]
        cluster_points[cluster_id] += 1
        new_centers[cluster_id, :] += m[i, :]  #############

    for i in range(k):
        new_centers[i] = new_centers[i] / cluster_points[i]
    return new_centers

#聚类，贴标签
def clustering(m, classifications, cur_centers):
    num_centers = cur_centers.shape[0]
    num_points = m.shape[0]
    for i in range(num_points):
        min = float('inf')
        tag = None
        for j in range(num_centers):
            dist = distance(m[i], cur_centers[j])
            if dist < min:
                min = dist
                tag = j
        classifications[i] = tag
    new_centers = cal_center(m, classifications, num_centers)
    return new_centers

'''
计算误差
存在某个中心点超出误差限返回True，表示误差不足以忽略
否则返回False，表示误差足够小，可以忽略
'''
def cal_error(new_centers, cur_centers, k, eps):
    for i in range(k):
        if math.sqrt(distance(new_centers[i], cur_centers[i])) > eps:
            return True
    return False

def k_means(m, k, eps):
    n_points = m.shape[0]
    cur_centers = m[0:k, :]
    classifications = [-1] * n_points
    new_centers = clustering(m, classifications, cur_centers)
    i = 0
    while cal_error(new_centers, cur_centers, k, eps):
        #print('cur_centers', cur_centers)
        #print('new_centers', new_centers)
        print(i)
        i = i + 1
        cur_centers = new_centers.copy()
        new_centers = clustering(m, classifications, cur_centers)

    return classifications