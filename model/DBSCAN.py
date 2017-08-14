import numpy as np
import math

UNCLASSIFIED = None
NOISE = -1

#计算两个点之间的距离
def distance(p, q):
    return math.sqrt(np.power(p - q, 2).sum())

#判断一个点是否在另一个点邻域内
def eps_neighborhood(p, q, eps):
    return distance(p, q) < eps

#搜索一个点的领域内所有点
def region_query(m, point_id, eps):
    n_points = m.shape[0]
    seeds = []
    for i in range(0, n_points):
        if eps_neighborhood(m[point_id, :], m[i, :], eps):
            seeds.append(i)
    return seeds

#添加标签
def expand_cluster(m, classifications, point_id, cluster_id, eps, min_points, visited):
    seeds = region_query(m, point_id, eps)
    visited[point_id] = True
    #非核心点，不贴标签，暂时标记为噪点
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    #核心点，将范围内的所有点贴上标签，并扩展范围内的其他核心点
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id
        while len(seeds) > 0:
            i = 0
            current_point = seeds[i]
            while i < len(seeds):
                if visited[i] == False:
                    current_point = seeds[i]
                    break
                i = i + 1
            if i == len(seeds):
                break
            seeds = seeds[i:]
            results = region_query(m, current_point, eps)
            if len(results) >= min_points:
                for i in range(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or classifications[result_point] == NOISE:
                        if classifications[result_point] == UNCLASSIFIED:
                            seeds.append(result_point)
                        classifications[result_point] = cluster_id
        return True


def dbscan(m, eps, min_points):
    cluster_id = 0
    n_points = m.shape[0]
    classifications = [UNCLASSIFIED] * n_points
    visited = [False] * n_points
    for point_id in range(0, n_points):
        if classifications[point_id] == UNCLASSIFIED:
            if expand_cluster(m, classifications, point_id, cluster_id, eps, min_points, visited):
                cluster_id = cluster_id + 1
    return classifications