import sys
sys.path.append(r'../../RScode/RS_AE/RSA')

import os
import numpy as np
from implicit_mf import implicit_mf
from model.bias_svd import BiasSVD


class implicit_biasSVD(implicit_mf):
    """
    docstring for BiasSVD
    implement the BiasSVD

    Koren Y, Bell R, Volinsky C. Matrix factorization techniques for recommender systems[J]. Computer, 2009, 42(8).
    """

    def __init__(self,k,data_path):
        super(implicit_biasSVD, self).__init__(k,data_path)
        self.config.lambdaB = 0.001  # 偏置项系数
        # self.init_model()

        
    def init_model(self, k):
        super(implicit_biasSVD, self).init_model(k)
        self.Bu = np.random.rand(self.rg.get_train_size()[0]) / (self.config.factor ** 0.5)  # bias value of user
        self.Bi = np.random.rand(self.rg.get_train_size()[1]) / (self.config.factor ** 0.5)  # bias value of item

    def train_model(self, k):
        super(implicit_biasSVD, self).train_model(k)
        iteration = 0
        while iteration < self.config.maxIter:
            self.loss = 0
            for index, line in enumerate(self.rg.trainSet(k)):
                user, item, rating = line
                u = self.rg.user[user]  # index u
                i = self.rg.item[item]  # index i
                error = rating - self.predict(user, item)
                self.loss += error ** 2
                p, q = self.P[u], self.Q[i]  # pu qi
                # update latent vectors

                self.Bu[u] += self.config.lr * (error - self.config.lambdaB * self.Bu[u])  # 更新bias u
                self.Bi[i] += self.config.lr * (error - self.config.lambdaB * self.Bi[i])  # 更新bias i

                self.P[u] += self.config.lr * (error * q - self.config.lambdaP * p)  # 更新pu
                self.Q[i] += self.config.lr * (error * p - self.config.lambdaQ * q)  # 更新qi

            self.loss += self.config.lambdaP * (self.P * self.P).sum() + self.config.lambdaQ * (self.Q * self.Q).sum() \
                         + self.config.lambdaB * ((self.Bu * self.Bu).sum() + (self.Bi * self.Bi).sum())
            
            iteration += 1
            
            if self.isConverged(iteration):
                break

    def predict(self, u, i):
        # super(BasicMFwithR, self).predict()
        if self.rg.containsUser(u) and self.rg.containsItem(i):
            u = self.rg.user[u]
            i = self.rg.item[i]
            return self.P[u].dot(self.Q[i]) + self.rg.globalMean + self.Bi[i] + self.Bu[u]  # q^T * Pu + u + bu + bi
        else:
            return self.rg.globalMean

    def recommend(self, user, num_items=10):
        recommend_dict={}
        for item in self.rg.all_Item.keys():
            prediction = self.predict(user, item)  # 预测-返回一个分数
            if item not in self.rg.trainSet_u[user]:
                recommend_dict[item]=prediction
        recommend_list=sorted(recommend_dict.items(),key=lambda item:item[1],reverse=True)
        return recommend_list[:num_items]