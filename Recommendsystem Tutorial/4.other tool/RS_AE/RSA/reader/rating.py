# encoding:utf-8
import sys

sys.path.append("..")
import os
from collections import defaultdict
import numpy as np

from utility.tools import normalize


class RatingGetter(object):
    """
    docstring for RatingGetter
    read rating data and save the global parameters
    """

    def __init__(self, k, config):
        super(RatingGetter, self).__init__()  # 继承..
        self.k_current = k  # 引入k
        self.config = config
        self.user = {}
        self.item = {}
        self.all_User = {}
        self.all_Item = {}
        self.id2user = {}
        self.id2item = {}
        self.dataSet_u = defaultdict(dict)
        self.trainSet_u = defaultdict(dict)
        self.trainSet_i = defaultdict(dict)
        self.testSet_u = defaultdict(dict)  # used to store the test set by hierarchy user:[item,rating]
        self.testSet_i = defaultdict(dict)  # used to store the test set by hierarchy item:[user,rating]
        self.testColdUserSet_u = defaultdict(dict)  # cold start users in test set
        self.trainHotUserSet = []  # hot users in train set
        self.trainSetLength = 0
        self.testSetLength = 0

        self.userMeans = {}  # used to store the mean values of users's ratings
        self.itemMeans = {}  # used to store the mean values of items's ratings
        self.globalMean = 0

        self.generate_data_set(k)  # generate train and test set
        self.getDataSet(k)
        self.get_data_statistics()
        self.get_cold_start_users()

    def generate_data_set(self, k):
        for index, line in enumerate(self.trainSet(k)):  # get测试集数据 e.g. index = 1, line = (a,b,c)
            u, i, r = line
            # print(u,i,r)
            if not u in self.user:
                self.user[u] = len(self.user)  # user_id反向字典={user_id:index}
                self.id2user[self.user[u]] = u  # user_id正向字典={index:user_id}
            if not i in self.item:
                self.item[i] = len(self.item)  # item_id反向字典={item_id:index}
                self.id2item[self.item[i]] = i  # item_id正向字典={index:item_id}

            self.trainSet_u[u][i] = r  # 双重dict {u:{i:r,...},...}
            self.trainSet_i[i][u] = r  # 双重dict {i:{u:r,...},...}
            self.trainSetLength = index + 1
        self.all_User.update(self.user)  # 更新all_user字典
        self.all_Item.update(self.item)  # 更新all_item字典

        for index, line in enumerate(self.testSet(k)):
            u, i, r = line
            if not u in self.user:
                self.all_User[u] = len(self.all_User)  # 更新all_user字典
            if not i in self.item:
                self.all_Item[i] = len(self.all_Item)  # 更新all_item字典
            self.testSet_u[u][i] = r  # 双重dict {u:{i:r,...},...}
            self.testSet_i[i][u] = r  # 双重dict {i:{u:r,...},...}
            self.testSetLength = index + 1
        pass

    # for cross validation
    def trainSet(self, k):
        # k = self.k_current  # 初始化k值
        for i in range(self.config.k_fold_num):  # k_文件数
            if i != k:  # 非k测试集
                data_path = self.config.rating_cv_path + self.config.dataset_name + "-" + str(i) + ".csv"
                # if not os.path.exists
                if not os.path.isfile(data_path):
                    print("the format of ratings data is wrong!")
                    sys.exit()
                with open(data_path, 'r') as f:  # 读取文件 获取数据
                    for index, line in enumerate(f):
                        u, i, r = line.strip('\r\n').split(self.config.sep)  # ['1.0', '3.0', '3.5']
                        r = normalize(float(r))  # scale the rating score to [0-1]
                        yield (int(float(u)), int(float(i)), float(r))  # 将trainSet 做成迭代器

    def testSet(self, k):
        # k = self.k_current  # k为测试集编号
        data_path = self.config.rating_cv_path + self.config.dataset_name + "-" + str(k) + ".csv"
        if not os.path.isfile(data_path):
            print("the format of ratings data is wrong!")
            sys.exit()
        with open(data_path, 'r') as f:  # 读取文件 获取数据
            for index, line in enumerate(f):
                u, i, r = line.strip('\r\n').split(self.config.sep)
                yield (int(float(u)), int(float(i)), float(r))  # 将testSet 做成迭代器

    # for random
    # def trainSet(self):
    #     np.random.seed(self.config.random_state)
    #     with open(self.config.rating_path,'r') as f:
    #         for index,line in enumerate(f):
    #             rand_num=np.random.rand()
    #             if  rand_num < self.config.size:
    #                 u,i,r=line.strip('\r\n').split(self.config.sep)
    #                 r=normalize(float(r)) #scale the rating score to [0-1]
    #                 yield (int(u),int(i),float(r))

    # def testSet(self):
    #     np.random.seed(self.config.random_state)
    #     with open(self.config.rating_path,'r') as f:
    #         for index,line in enumerate(f):
    #             rand_num=np.random.rand()
    #             if  rand_num >= self.config.size:
    #                 u,i,r=line.strip('\r\n').split(self.config.sep)
    #                 yield (int(u),int(i),float(r))

    def getDataSet(self, k):  # 获取原始数据dataSet_u
        with open(self.config.rating_path, 'r') as f:
            for index, line in enumerate(f):
                u, i, r = line.strip('\r\n').split(self.config.sep)
                self.dataSet_u[int(u)][int(i)] = float(r)

    def get_train_size(self):  # 获取数据size(u,i)
        return (len(self.user), len(self.item))

    # get cold start users in test set
    def get_cold_start_users(self):
        for user in self.testSet_u.keys():
            rating_length = len(self.trainSet_u[user])
            if rating_length <= self.config.coldUserRating:  # 冷启动Rating 默认为5
                self.testColdUserSet_u[user] = self.testSet_u[user]
        print('cold start users count', len(self.testColdUserSet_u))

    def get_data_statistics(self):  # 数据统计

        total_rating = 0.0  # 总分
        total_length = 0  # 总长度
        for u in self.user:
            u_total = sum(self.trainSet_u[u].values())  # 用户对物品的所有评分加和
            u_length = len(self.trainSet_u[u])  # 用户评过的物品数
            total_rating += u_total  # 所有用户加和
            total_length += u_length
            self.userMeans[u] = u_total / float(u_length)  # 对每个用户 用户总分/用户评分物品数

        for i in self.item:  # 对每个物品 求平均分
            self.itemMeans[i] = sum(self.trainSet_i[i].values()) / float(len(self.trainSet_i[i]))

        if total_length == 0:
            self.globalMean = 0
        else:
            self.globalMean = total_rating / total_length  # 总体平均分

    def containsUser(self, u):
        'whether user is in training set'
        if u in self.user:
            return True
        else:
            return False

    def containsItem(self, i):
        'whether item is in training set'
        if i in self.item:
            return True
        else:
            return False

    def containsUserItem(self, user, item):
        if user in self.trainSet_u:
            if item in self.trainSet_u[user]:
                # print(user)
                # print(item)
                # print(self.trainSet_u[user][item])
                return True
        return False

    def get_row(self, u):  # 获取某行
        return self.trainSet_u[u]

    def get_col(self, c):  # 获取某列
        return self.trainSet_i[c]

    def user_rated_items(self, u):
        return self.trainSet_u[u].keys()


if __name__ == '__main__':
    rg = RatingGetter(0)
    # for ind,entry in enumerate(rg.testSet()):
    # 	if ind<80:
    # 		print(entry)
    # # 		user,item,rating = entry

    # print(rg.trainSet_u[52])
    # print(rg.trainSet_u[10])
