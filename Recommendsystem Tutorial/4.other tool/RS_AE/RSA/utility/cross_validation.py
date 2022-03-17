# encoding:utf-8
import sys

sys.path.append("..")
import os
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from configx.configx import ConfigX

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Split ratings into five folds
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def split_5_folds(configx):
    K = configx.k_fold_num  # 分的组数 默认为5
    names = ['user_id', 'item_id', 'rating']  # 标签名
    if not os.path.isfile(configx.rating_path):  # 若没有文件，则报错
        print("the format of rating data is wrong")
        sys.exit()
    df = pd.read_csv(configx.rating_path, sep=configx.sep, names=names)  # 读取文件为DataFrame,列名为names 35497 * 3
    ratings = coo_matrix((df.rating, (df.user_id, df.item_id)))  # 将dataFrame转换为 (x,y) value 的矩阵格式
    users = np.unique(ratings.row)  # 获取所有用户
    ratings = ratings.tocsr()  # 将矩阵进行csr转换，用于节省内存

    rows = list()  # 初始化 行
    cols = list()  # 初始化 列
    vals = list()  # 初始化 值
    nonzeros = list()  # 初始化 每组数据的非零值数目

    for k in range(K):
        size_of_bucket = int(ratings.nnz / K)  # 将非零数据总数分为均等的5(K)份
        if k == K - 1:
            size_of_bucket += ratings.nnz % K  # 最后一份数据 加上 多出来的数据
        rows.append(np.zeros(size_of_bucket))  # 行数据 添加 初始值
        cols.append(np.zeros(size_of_bucket))  # 列数据 添加 初始值
        vals.append(np.zeros(size_of_bucket))  # value 添加 初始值
        nonzeros.append(0)  # 非零项 添加 初始值

    for i, user in enumerate(users):  # 对于每个用户 i 为 index, user 为用户编号，区别是两个值相差一 如 i = 0, user = 1
        items = ratings[user, :].indices  # 每位用户的item列表
        rating_vals = ratings[user, :].data  # 每位用户的评分
        index_list = [i for i in range(K)] * int(len(items) / float(K) + 1)  # 将item列表 分为n组index [0 1 2 3 4]
        np.random.shuffle(index_list)  # 将index的顺序打乱
        index_list = np.array(index_list)  # 将list转换为array 用于后面的bool操作

        for k in range(K):
            k_index_list = (index_list[:len(items)] == k)  # 获取与k相对应的 长度为items 的index bool数组
            from_ind = nonzeros[k]  # 将已有的非零数目 作为初始index
            to_ind = nonzeros[k] + sum(k_index_list)  # 将已有的非零数目 加上新增的数目 作为末尾index

            if to_ind >= len(rows[k]):  # 若末尾数目超出了原有的行空间 则新增行空间
                rows[k] = np.append(rows[k], np.zeros(size_of_bucket))  # 行增空间
                cols[k] = np.append(cols[k], np.zeros(size_of_bucket))  # 列增空间
                vals[k] = np.append(vals[k], np.zeros(size_of_bucket))  # 值增空间
                k_index_list = (index_list[:len(items)] == k)  # index重新分配 bool数组

            rows[k][from_ind:to_ind] = [user] * sum(k_index_list)  # 将第k行的 值 设为对应长度的 user_id
            cols[k][from_ind:to_ind] = items[k_index_list]  # 将第k列的 值 设为对应长度的 item_id
            vals[k][from_ind:to_ind] = rating_vals[k_index_list]  # 将第k行 值 设为对应长度的 value
            nonzeros[k] += sum(k_index_list)  # 非零个数增加

    if not os.path.exists('../data/cv'):  # 如果没有cv路径，则创建路径
        os.makedirs('../data/cv')
        print('../data/cv folder has been established.')

    for k, (row, col, val, nonzero) in enumerate(zip(rows, cols, vals, nonzeros)):
        bucket_df = pd.DataFrame({'user': row[:nonzero], 'item': col[:nonzero], 'rating': val[:nonzero]},
                                 columns=['user', 'item', 'rating'])
        bucket_df.to_csv("../data/cv/%s-%d.csv" % (configx.dataset_name, k), sep=configx.sep, header=False, index=False)
        print("%s -fold%d data generated finished!" % (configx.dataset_name, k))

    print("All Data Generated Done!")


if __name__ == "__main__":
    configx = ConfigX()
    split_5_folds(configx)
