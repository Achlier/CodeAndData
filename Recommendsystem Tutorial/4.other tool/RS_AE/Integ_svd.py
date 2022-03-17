import sys

sys.path.append(r'RSA/')
sys.path.append(r'RSA')
from RSA import run_func
import numpy as np
from collections import defaultdict


class Integ_svd:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.read_rating(rs)
        rs.Bu = np.random.rand(rs.rg.get_train_size()[0]) / (rs.rg.config.factor ** 0.5)
        rs.Bi = np.random.rand(rs.rg.get_train_size()[1]) / (rs.rg.config.factor ** 0.5)
        rs.P = np.random.rand(rs.rg.get_train_size()[0], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        rs.Q = np.random.rand(rs.rg.get_train_size()[1], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        rs.user_item_nei = defaultdict(dict)
        rs.W = np.random.rand(rs.rg.get_train_size()[1], rs.rg.get_train_size()[1])
        rs.item_near_num = 10
        rs.config.lambdaP = 0.001
        rs.config.lambdaQ = 0.001
        rs.lambdaB = 0.01
        rs.lambdaW = 0.01

    def train_model(self, rs, k):
        iteration = 0
        while iteration < rs.config.maxIter:
            rs.loss = 0
            for index, line in enumerate(rs.rg.trainSet(k)):
                user, item, rating = line
                u = rs.rg.user[user]
                i = rs.rg.item[item]
                ui_neighbors = self.get_neighbor(rs, user, item)
                ui_nei_len = len(ui_neighbors)
                error = rating - rs.predict_rs(rs, u=user, i=item)
                rs.loss += error ** 2

                p, q = rs.P[u], rs.Q[i]
                # nu, sum_y = self.get_sum_y(user)

                # update latent vectors
                rs.Bu[u] += rs.rg.config.lr * (error - rs.lambdaB * rs.Bu[u])
                rs.Bi[i] += rs.rg.config.lr * (error - rs.lambdaB * rs.Bi[i])

                rs.P[u] += rs.rg.config.lr * (error * q - rs.rg.config.lambdaP * p)
                rs.Q[i] += rs.rg.config.lr * (error * p - rs.rg.config.lambdaQ * q
                                              )  # + sum_y

                for neighbor in ui_neighbors:
                    j = rs.rg.item[neighbor]
                    ruj = rs.rg.trainSet_u[user][neighbor]
                    buj = rs.rg.globalMean + rs.Bu[u] + rs.Bi[j]
                    rs.W[i][j] += rs.rg.config.lr * (error / (ui_nei_len ** 0.5) *
                                                     (ruj - buj) -
                                                     rs.lambdaW * rs.W[i][j])

            rs.loss += rs.rg.config.lambdaP * (rs.P * rs.P).sum(
            ) + rs.rg.config.lambdaQ * (rs.Q * rs.Q).sum() + rs.lambdaB * (
                               (rs.Bu * rs.Bu).sum() +
                               (rs.Bi * rs.Bi).sum()) + rs.lambdaW * (rs.W * rs.W).sum()
            iteration += 1
            if rs.isConverged_rs(iteration, rs, k):  # 判断converge
                break

    def predict(self, rs, u, i):
        user = u
        item = i
        if rs.rg.containsUser(user) and rs.rg.containsItem(item):
            # _, sum_y = self.get_sum_y(user)
            sum_w = 0.0
            u = rs.rg.user[user]  # index u
            i = rs.rg.item[item]  # index i
            bui = rs.rg.globalMean + rs.Bi[i] + rs.Bu[u]  # baseline 评分
            ui_neighbors = self.get_neighbor(rs, user, item)  # 获取neighbor tuple
            ui_len = len(ui_neighbors)  # 获取neighbor 数量
            for neighbor in ui_neighbors:
                j = rs.rg.item[neighbor]  # index j
                ruj = rs.rg.trainSet_u[user][neighbor]  # u对j的评分
                buj = rs.rg.globalMean + rs.Bi[j] + rs.Bu[u]  # baseline 评分
                sum_w += (ruj - buj) * rs.W[i][j]  # +self.C[i][j]
            if ui_len != 0:
                sum_w *= 1.0 / ui_len  # 这的事
            return bui + rs.Q[i].dot(rs.P[u]) + sum_w  # + sum_y
        else:
            return rs.rg.globalMean

    def get_neighbor(self, rs, user, item):  # 获取邻居
        if user in rs.user_item_nei and item in rs.user_item_nei[user]:  # 如果用户有邻居且用户的邻居里有该物品
            return rs.user_item_nei[user][item]  # 直接返回item_id tuple
        items = rs.rg.user_rated_items(user)  # 返回该用户评过分的物品列表 {i:r,i:r...}
        u_item_d = {}
        for u_item in items:
            if item != u_item:
                sim = rs.get_pearson(rs.rg.get_col(item), rs.rg.get_col(u_item))  # 计算similarity
                u_item_d[u_item] = round(sim, 4)  # 收集similarity 保留4位小数
        matchItems = sorted(u_item_d.items(), key=lambda x: x[1], reverse=True)[
                     :rs.item_near_num]  # [(18, array([0.99337203])), (95, array([0.98155102]))
        matchItems = list(zip(*matchItems))  # [(18,95),(array([]),array([]))]
        if len(matchItems) > 0:  # 有匹配的话
            rs.user_item_nei[user][item] = matchItems[0]  # {u:{i:()}}
            return matchItems[0]  # 返回tuple
        else:
            return []  # 没有就返回空表

    def recommend(self, rs, user, num_items=5):
        recommend_dict = {}
        for item in rs.rg.all_Item.keys():
            prediction = self.predict(rs, user, item)  # 预测-返回一个分数
            if item not in rs.rg.trainSet_u[user]:
                recommend_dict[item] = prediction
        recommend_list = sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True)
        return recommend_list[:num_items]
