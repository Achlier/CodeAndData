import sys

sys.path.append(r'RSA/')
sys.path.append(r'RSA')
from RSA import run_func
import numpy as np


class PMF:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.read_rating(rs)
        rs.P = np.random.rand(rs.rg.get_train_size()[0], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        rs.Q = np.random.rand(rs.rg.get_train_size()[1], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        rs.rg.config.lambdaP = 0.001  # 初始化lambdaP
        rs.rg.config.lambdaQ = 0.001  # 初始化lambdaQ
        rs.rg.config.gamma = 0.9  # Momentum
        rs.rg.config.isEarlyStopping = True  # ？

    def train_model(self, rs, k):
        iteration = 0  # 循环记数
        p_delta, q_delta = dict(), dict()
        while iteration < rs.rg.config.maxIter:  # 默认100
            rs.loss = 0  # cost初始化
            for index, line in enumerate(rs.rg.trainSet(k)):  # 从训练集提取数据
                user, item, rating = line
                u = rs.rg.user[user]  # user对应的index
                i = rs.rg.item[item]  # item对应的index
                pred = rs.predict_rs(rs, u=user, i=item)

                error = rating - pred  # self.predict(user,item)
                rs.loss += error ** 2  # loss = sum((rating - prediction)^2)
                p, q = rs.P[u], rs.Q[i]  # 获取latent vectors
                # update latent vectors

                if not u in p_delta:  # 初始化 p_delta
                    p_delta[u] = np.zeros(rs.rg.config.factor)
                if not i in q_delta:  # 初始化 q_delta
                    q_delta[i] = np.zeros(rs.rg.config.factor)
                # 加入正则化的costFunction
                p_delta[u] = rs.rg.config.lr * (-error * q + rs.rg.config.lambdaP * p) + rs.rg.config.gamma * p_delta[u]
                q_delta[i] = rs.rg.config.lr * (-error * p + rs.rg.config.lambdaQ * q) + rs.rg.config.gamma * q_delta[i]
                rs.P[u] -= p_delta[u]  # 更新评分(delta)_Gradient_descent
                rs.Q[i] -= q_delta[i]  # 更新评分（delta)_Gradient_descent
            # 最终的目标函数+两项正则项
            rs.loss += rs.rg.config.lambdaP * (rs.P * rs.P).sum() + rs.rg.config.lambdaQ * (rs.Q * rs.Q).sum()

            iteration += 1
            if rs.isConverged_rs(iteration, rs, k):  # 判断converge
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
