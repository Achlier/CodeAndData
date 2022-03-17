# encoding:utf-8
import sys

sys.path.append("..")
from prettyprinter import cpprint
import numpy as np
from model.mf import MF
from collections import defaultdict
from utility.similarity import pearson_sp
from utility import util


class IntegSVD(MF):
    """
    docstring for IntegSVD
    implement the IntegSVD

    Koren Y. Factor in the neighbors: Scalable and accurate collaborative filtering[J]. ACM Transactions on Knowledge Discovery from Data (TKDD), 2010, 4(1): 1.
    """

    def __init__(self, k):
        super(IntegSVD, self).__init__(k)  # 继承MF

        # self.config.lr=0.001
        # self.config.maxIter=200 #400
        self.config.item_near_num = 10  # 10

        self.config.lambdaP = 0.001
        self.config.lambdaQ = 0.001

        # self.config.lambdaY = 0.01
        self.config.lambdaB = 0.01

        self.config.lambdaW = 0.01
        # self.config.lambdaC = 0.015
        # self.init_model()

    def init_model(self, k):
        super(IntegSVD, self).init_model(k)  # 载入数据，初始化
        # Bu = [] Bi = []
        self.Bu = np.random.rand(self.rg.get_train_size()[0]) / (self.config.factor ** 0.5)  # bias value of user
        self.Bi = np.random.rand(self.rg.get_train_size()[1]) / (self.config.factor ** 0.5)  # bias value of item
        # self.Y = np.random.rand(self.rg.get_train_size()[1], self.config.factor) / (self.config.factor ** 0.5)  # implicit preference

        self.user_item_nei = defaultdict(dict)
        self.W = np.random.rand(self.rg.get_train_size()[1], self.rg.get_train_size()[1])
        # self.C=np.random.rand(self.rg.get_train_size()[1],self.rg.get_train_size()[1])

        # print('initializinig neighbors')
        # for user in self.rg.trainSet_u:
        #     for item in self.rg.trainSet_u[user]:
        #         self.get_neighbor(user,item)

    def train_model(self, k):
        super(IntegSVD, self).train_model(k)
        iteration = 0
        while iteration < self.config.maxIter:
            self.loss = 0
            for index, line in enumerate(self.rg.trainSet(k)):
                user, item, rating = line
                u = self.rg.user[user]  # user index
                i = self.rg.item[item]  # item index
                ui_neighbors = self.get_neighbor(user, item)  # return item_id tuple: (i1,i2...)
                ui_nei_len = len(ui_neighbors)  # neighbor数量
                error = rating - self.predict(user, item)  # error
                self.loss += error ** 2  # loss

                p, q = self.P[u], self.Q[i]  # Pu, Qi
                # nu, sum_y = self.get_sum_y(user)

                # update latent vectors
                self.Bu[u] += self.config.lr * (error - self.config.lambdaB * self.Bu[u])
                self.Bi[i] += self.config.lr * (error - self.config.lambdaB * self.Bi[i])

                self.P[u] += self.config.lr * (error * q - self.config.lambdaP * p)
                self.Q[i] += self.config.lr * (error * p - self.config.lambdaQ * q)  # + sum_y

                # 更新Y
                # u_items = self.rg.user_rated_items(u)
                # for j in u_items:
                #     idj = self.rg.item[j]
                #     self.Y[idj] += self.config.lr * (error / np.sqrt(nu) * q - self.config.lambdaY * self.Y[idj])
                # 更新W,C
                for neighbor in ui_neighbors:
                    j = self.rg.item[neighbor]  # neighbor index j
                    ruj = self.rg.trainSet_u[user][neighbor]  # user 对 neighbor 的评分
                    buj = self.rg.globalMean + self.Bu[u] + self.Bi[j]  # baseline
                    self.W[i][j] += self.config.lr * (
                            error / (ui_nei_len ** 0.5) * (ruj - buj) - self.config.lambdaW * self.W[i][j])
                    # self.C[i][j] += self.config.lr * (error / (ui_nei_len ** 0.5) - self.config.lambdaC * self.C[i][j])

            self.loss += self.config.lambdaP * (self.P * self.P).sum() + self.config.lambdaQ * (self.Q * self.Q).sum() \
                         + self.config.lambdaB * ( \
                                     (self.Bu * self.Bu).sum() + (self.Bi * self.Bi).sum()) + self.config.lambdaW * (
                                 self.W * self.W).sum()  # + self.config.lambdaY * (self.Y * self.Y).sum() \
            # +self.config.lambdaC * (self.C * self.C).sum()
            iteration += 1
            if self.isConverged(iteration):  # 判断converge
                break

        util.save_data(self.user_item_nei, '../data/neibor/ft_intsvd_useritemnei_08.pkl')

    def predict(self, user, item):
        if self.rg.containsUser(user) and self.rg.containsItem(item):
            # _, sum_y = self.get_sum_y(user)
            sum_w = 0.0
            u = self.rg.user[user]  # index u
            i = self.rg.item[item]  # index i
            bui = self.rg.globalMean + self.Bi[i] + self.Bu[u]  # baseline 评分
            ui_neighbors = self.get_neighbor(user, item)  # 获取neighbor tuple
            ui_len = len(ui_neighbors)  # 获取neighbor 数量
            for neighbor in ui_neighbors:
                j = self.rg.item[neighbor]  # index j
                ruj = self.rg.trainSet_u[user][neighbor]  # u对j的评分
                buj = self.rg.globalMean + self.Bi[j] + self.Bu[u]  # baseline 评分
                sum_w += (ruj - buj) * self.W[i][j]  # +self.C[i][j]
            if ui_len != 0:
                sum_w *= 1.0 / ui_len  # 这的事
            return bui + self.Q[i].dot(self.P[u]) + sum_w  # + sum_y
        else:
            return self.rg.globalMean

    def get_sum_y(self, u):
        u_items = self.rg.user_rated_items(u)  # u评分的 item_id
        nu = len(u_items)
        sum_y = np.zeros(self.config.factor)
        for j in u_items:
            sum_y += self.Y[self.rg.item[j]]
        sum_y /= (np.sqrt(nu))
        return nu, sum_y

    def get_neighbor(self, user, item):  # 获取邻居
        if user in self.user_item_nei and item in self.user_item_nei[user]:  # 如果用户有邻居且用户的邻居里有该物品
            return self.user_item_nei[user][item]  # 直接返回item_id tuple
        items = self.rg.user_rated_items(user)  # 返回该用户评过分的物品列表 {i:r,i:r...}
        u_item_d = {}
        for u_item in items:
            if item != u_item:
                sim = pearson_sp(self.rg.get_col(item), self.rg.get_col(u_item))  # 计算similarity
                u_item_d[u_item] = round(sim, 4)  # 收集similarity 保留4位小数
        matchItems = sorted(u_item_d.items(), key=lambda x: x[1], reverse=True)[
                     :self.config.item_near_num]  # [(18, array([0.99337203])), (95, array([0.98155102]))
        matchItems = list(zip(*matchItems))  # [(18,95),(array([]),array([]))]
        if len(matchItems) > 0:  # 有匹配的话
            self.user_item_nei[user][item] = matchItems[0]  # {u:{i:()}}
            return matchItems[0]  # 返回tuple
        else:
            return []  # 没有就返回空表


if __name__ == '__main__':
    rmses = []
    bmf = IntegSVD(0)
    # print(bmf.rg.trainSet_u[1])
    for i in range(bmf.config.k_fold_num):
        bmf.train_model(i)
        rmse, mae = bmf.predict_model()
        rmses.append(rmse)
    print(rmses)
    # bmf.config.k_current = 1
    # print(bmf.rg.trainSet_u[1])
    # bmf.train_model()
    # bmf.predict_model()
