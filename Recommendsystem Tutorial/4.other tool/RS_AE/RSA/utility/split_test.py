# encoding:utf-8
import sys

sys.path.append("..")
import os
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from configx.configx import ConfigX
from utility.tools import normalize
from collections import defaultdict

config = ConfigX()
names = ['user_id', 'item_id', 'rating']
df = pd.read_csv(config.rating_path, sep=config.sep, names=names)
# print(df[df.user_id == 1])
#    user_id  item_id  rating
# 0        1        1     2.0
# 1        1        2     4.0
# 2        1        3     3.5
# 3        1        4     3.0
# 4        1        5     4.0
ratings = coo_matrix((df.rating, (df.user_id, df.item_id)))
# print(ratings)
#   (1508, 486)	2.5
#   (1508, 84)	3.5
#   (1508, 17)	4.0
#   (1508, 669)	1.0
#   (1508, 686)	2.5
#   (1508, 806)	3.5
users = np.unique(ratings.row)
# print(users)
# [   1    2    3 ... 1506 1507 1508]
ratings = ratings.tocsr()
# print(ratings) 用于节省内存
#   (1508, 486)	2.5
#   (1508, 84)	3.5
#   (1508, 17)	4.0
#   (1508, 669)	1.0
#   (1508, 686)	2.5
#   (1508, 806)	3.5
# print(ratings.nnz)  # 非零个数 35494
rows = list()
cols = list()
vals = list()
nonzeros = list()
K = config.k_fold_num  # K = 5

for k in range(K):
    size_of_bucket = int(ratings.nnz / K)
    if k == K - 1:
        size_of_bucket += ratings.nnz % K
    rows.append(np.zeros(size_of_bucket))
    cols.append(np.zeros(size_of_bucket))
    vals.append(np.zeros(size_of_bucket))
    nonzeros.append(0)
# print(rows) [array([0., 0., 0., ..., 0., 0., 0.]),...] (5*len(nnz))
# 7098
# 7098
# 7098
# 7098
# 7102
# print(nonzeros) [0, 0, 0, 0, 0]

items = ratings[1, :].indices
# ratings[1, :]
#   (0, 1)	2.0
#   (0, 2)	4.0
#   (0, 3)	3.5
#   (0, 4)	3.0
#   (0, 5)	4.0
#   (0, 6)	3.5
#   (0, 7)	3.5
#   (0, 8)	3.0
#   (0, 9)	2.5
#   (0, 10)	4.0
#   (0, 11)	4.0
#   (0, 12)	4.0
# print(items)
# [ 1  2  3  4  5  6  7  8  9 10 11 12]
rating_vals = ratings[1, :].data
# print(rating_vals)
# [2.  4.  3.5 3.  4.  3.5 3.5 3.  2.5 4.  4.  4. ]
index_list = [i for i in range(K)] * int(len(items) / float(K) + 1)
# print(index_list)
# [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
np.random.shuffle(index_list)  # 将列表随机排序
# print(index_list)
# [0, 4, 0, 1, 2, 2, 0, 3, 4, 4, 3, 3, 1, 2, 1]
index_list = np.array(index_list)  # 转为array，后面要用到bool
k = 1
k_index_list = (index_list[:len(items)] == k)
# print(k_index_list)
from_ind = nonzeros[k]
to_ind = nonzeros[k] + sum(k_index_list)
# print(from_ind,to_ind)
# 0 3
if to_ind >= len(rows[k]):
    rows[k] = np.append(rows[k], np.zeros(size_of_bucket))
    cols[k] = np.append(cols[k], np.zeros(size_of_bucket))
    vals[k] = np.append(vals[k], np.zeros(size_of_bucket))
    k_index_list = (index_list[:len(items)] == k)
rows[k][from_ind:to_ind] = [1] * sum(k_index_list)
cols[k][from_ind:to_ind] = items[k_index_list]
vals[k][from_ind:to_ind] = rating_vals[k_index_list]
nonzeros[k] += sum(k_index_list)


# print(rows[1],cols[1],vals[1],nonzeros)
# [1. 1. 1. ... 0. 0. 0.] [ 2.  7. 10. ...  0.  0.  0.] [4.  3.5 4.  ... 0.  0.  0. ] [0, 3, 0, 0, 0]

# 训练集测试
def train():
    for i in range(config.k_fold_num):
        if i != k:
            data_path = config.rating_cv_path + config.dataset_name + "-" + str(i) + ".csv"
            with open(data_path, 'r') as f:  # 读取文件 获取数据
                for index, line in enumerate(f):
                    u, i, r = line.strip('\r\n').split(config.sep)
                    r = normalize(float(r))  # scale the rating score to [0-1]
                    yield (int(float(u)), int(float(i)), float(r))


# user = {}
# id2user = {}
# item = {}
# id2item = {}
# trainSet_u = defaultdict(dict)
# all_User = {}
# all_Item = {}
# for index, line in enumerate(train()):  # e.g. index = 1, line = (a,b,c)
#     u, i, r = line
#     if not u in user:
#         user[u] = len(user)
#         id2user[user[u]] = u
#     if not i in item:
#         item[i] = len(item)  # item_id反向字典={item_id:index}
#         id2item[item[i]] = i
#     trainSet_u[i][u] = r
#     all_User.update(user)  # 更新all_user字典
#     all_Item.update(item)  # 更新all_item字典


# print(user)
# print(id2user)
# # print(item)
# print(id2item)
# print(trainSet_u[1])

# 测试集测试
def test():
    data_path = config.rating_cv_path + config.dataset_name + "-" + str(k) + ".csv"
    with open(data_path, 'r') as f:  # 读取文件 获取数据
        for index, line in enumerate(f):
            u, i, r = line.strip('\r\n').split(config.sep)
            yield (int(float(u)), int(float(i)), float(r))


# testSet_u = defaultdict(dict)
# testSet_i = defaultdict(dict)
# for index, line in enumerate(test()):
#     u, i, r = line
#     if not u in user:
#         all_User[u] = len(all_User)
#     if not i in item:
#         all_Item[i] = len(all_Item)
#     testSet_u[u][i] = r
#     testSet_i[i][u] = r
#     testSetLength = index + 1
# print(all_User)

dataSet_u = defaultdict(dict)


# 直接获取数据测试
def getDataSet():
    with open(config.rating_path, 'r') as f:
        for index, line in enumerate(f):
            u, i, r = line.strip('\r\n').split(config.sep)
            dataSet_u[int(u)][int(i)] = float(r)


# a = np.random.rand(3000,10)/(10**0.5)
# b = np.random.rand(3000,10)/(10**0.5)
# print(a[1])
# c = np.array([1,2,3])
# d = np.array([1,2,3])
# print(c.dot(d))
# print(round(3,4))
# x1 = {1: 2, 2: 3, 3: 4, 4: 5}
# x2 = {1: 0, 2: 1, 3: 2, 4: 3}
# common = set(x1.keys()) & set(x2.keys())
# print(common)
# s1 = 2
# print(pow(s1,3))
symMatrix = {}

# def set(i, j, val):
#     if not i in symMatrix:
#         symMatrix[i] = {}
#     symMatrix[i][j] = val
#     if not j in symMatrix:
#         symMatrix[j] = {}
#     symMatrix[j][i] = val
#
#
# set(1, 2, 3)
# set(1, 3, 3)
# set(2, 2, 3)
# user_sim = symMatrix
# matchUsers = sorted(user_sim[1].items(), key=lambda x: x[1], reverse=True)
# print(user_sim)
# print(matchUsers)

# class A(object):
#     def __init__(self):
#         self.a = 0.0
#
#     def a(self, a):
#         self.a = a
#         print(a)
#
#
# class B(A):
#     def __init__(self):
#         super(B, self).__init__
#
#     def a(self, a):
#         super(B, self).a(a)
#         self.a = 11
#         print(self.a)
#
#
# b = B()
# b.a(9)  # output: 11

# print(np.random.rand(31))
# u_item_d = {}
# for i in range(100):
#     u_item_d[i] = np.random.rand(1)
#
# mi = sorted(u_item_d.items(), key=lambda x: x[1], reverse=True)[:10]
# mi = list(zip(*mi))
# print(mi[0])

sum_y = np.ones((4,5))
a = np.array([1,2,3])
b = np.array([2,3,4])
c = np.zeros(3)
d = np.random.seed(0)
print(d)