####Test 跑起来 Funk_svd 测试
import sys

sys.path.append(r'RSA/')
sys.path.append(r'RSA')
from RSA import run_func
import numpy as np


class Funk_svd:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.read_rating(rs)
        rs.P = np.random.rand(rs.rg.get_train_size()[0], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        rs.Q = np.random.rand(rs.rg.get_train_size()[1], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)

    def train_model(self, rs, k):
        iteration = 0
        while iteration < rs.rg.config.maxIter:
            rs.loss = 0
            for index, line in enumerate(rs.rg.trainSet(k)):
                user, item, rating = line
                u = rs.rg.user[user]
                i = rs.rg.item[item]
                error = rating - rs.predict_rs(rs, u=user, i=item)
                rs.loss += error ** 2
                p, q = rs.P[u], rs.Q[i]
                rs.P[u] += rs.rg.config.lr * error * q
                rs.Q[i] += rs.rg.config.lr * error * p
            iteration += 1
            if rs.isConverged_rs(iteration, rs, k):
                break

    def predict(self, rs, u, i):
        if rs.rg.containsUser(u) and rs.rg.containsItem(i):
            return rs.P[rs.rg.user[u]].dot(rs.Q[rs.rg.item[i]])  # 矩阵相乘user评分*item评分
        elif rs.rg.containsUser(u) and not rs.rg.containsItem(i):
            return rs.rg.userMeans[u]  # 若没有物品评分，则使用用户平均分
        elif not rs.rg.containsUser(u) and rs.rg.containsItem(i):
            return rs.rg.itemMeans[i]  # 若没有用户评分，则使用物品平均分
        else:
            return rs.rg.globalMean  # 若无任何评分(新物品)，则使用所有平均分

    def recommend(self, rs, user, num_items=5):
        recommend_dict = {}
        for item in rs.rg.all_Item.keys():
            prediction = self.predict(rs, user, item)  # 预测-返回一个分数
            if item not in rs.rg.trainSet_u[user]:
                recommend_dict[item] = prediction
        recommend_list = sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True)
        return recommend_list[:num_items]
