import sys

sys.path.append(r'RSA/')
sys.path.append(r'RSA')
from RSA import run_func
import numpy as np
from utility.tools import denormalize

class Bias_svd:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.read_rating(rs)
        rs.lambdaB = 0.001
        rs.rg.config.lambdaP = 0.001  # 初始化lambdaP
        rs.rg.config.lambdaQ = 0.001  # 初始化lambdaQ
        rs.P = np.random.rand(rs.rg.get_train_size()[0], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        rs.Q = np.random.rand(rs.rg.get_train_size()[1], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        rs.Bu = np.random.rand(rs.rg.get_train_size()[0]) / (rs.rg.config.factor ** 0.5)
        rs.Bi = np.random.rand(rs.rg.get_train_size()[1]) / (rs.rg.config.factor ** 0.5)

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
                # update latent vectors

                rs.Bu[u] += rs.rg.config.lr * (error - rs.lambdaB * rs.Bu[u])
                rs.Bi[i] += rs.rg.config.lr * (error - rs.lambdaB * rs.Bi[i])

                rs.P[u] += rs.rg.config.lr * (error * q - rs.rg.config.lambdaP * p)
                rs.Q[i] += rs.rg.config.lr * (error * p - rs.rg.config.lambdaQ * q)

            rs.loss += rs.rg.config.lambdaP * (rs.P * rs.P).sum() + rs.rg.config.lambdaQ * (rs.Q * rs.Q).sum() \
                       + rs.lambdaB * ((rs.Bu * rs.Bu).sum() + (rs.Bi * rs.Bi).sum())
            iteration += 1
            if rs.isConverged_rs(iteration, rs, k):
                break

    def predict(self, rs, u, i):
        if rs.rg.containsUser(u) and rs.rg.containsItem(i):
            u = rs.rg.user[u]
            i = rs.rg.item[i]
            return rs.P[u].dot(rs.Q[i]) + rs.rg.globalMean + rs.Bi[i] + rs.Bu[u]
        else:
            return rs.rg.globalMean

    def recommend(self, rs, user, num_items=5):
        recommend_dict = {}
        for item in rs.rg.all_Item.keys():
            prediction = self.predict(rs, user, item)  # 预测-返回一个分数
            if item not in rs.rg.trainSet_u[user]:
                recommend_dict[item] = prediction
        recommend_list = sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True)
        return recommend_list[:num_items]
