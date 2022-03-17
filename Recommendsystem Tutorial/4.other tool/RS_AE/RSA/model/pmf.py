# encoding:utf-8
import sys

sys.path.append("..")

from prettyprinter import cpprint, set_default_style
# set_default_style('light')
import numpy as np
from model.mf import MF
from utility import tools


class FunkSVDwithR(MF):
    """
    docstring for FunkSVDwithR
    implement the FunkSVD with regularization
    http://sifter.org/~simon/journal/20061211.html
    """

    def __init__(self, k):  #
        super(FunkSVDwithR, self).__init__(k)  # 继承MF
        self.config.lambdaP = 0.001  # 初始化lambdaP
        self.config.lambdaQ = 0.001  # 初始化lambdaQ
        self.config.gamma = 0.9  # Momentum
        self.config.isEarlyStopping = True  # ？
        # self.init_model()

    # def init_model(self):
    # 	super(FunkSVDwithR, self).init_model()

    def train_model(self, k):
        super(FunkSVDwithR, self).train_model(k)  # MF.init_model(k)
        iteration = 0  # 循环记数
        p_delta, q_delta = dict(), dict()
        while iteration < self.config.maxIter:  # 默认100
            self.loss = 0  # cost初始化
            for index, line in enumerate(self.rg.trainSet(k)):  # 从训练集提取数据
                user, item, rating = line
                u = self.rg.user[user]  # user对应的index
                i = self.rg.item[item]  # item对应的index
                pred = self.predict(u=user, i=item)
                # pred = tools.sigmoid(pred)
                error = rating - pred  # self.predict(user,item)
                self.loss += error ** 2  # loss = sum((rating - prediction)^2)
                p, q = self.P[u], self.Q[i]  # 获取latent vectors
                # update latent vectors 

                if not u in p_delta:  # 初始化 p_delta
                    p_delta[u] = np.zeros(self.config.factor)
                if not i in q_delta:  # 初始化 q_delta
                    q_delta[i] = np.zeros(self.config.factor)
                # 加入正则化的costFunction
                p_delta[u] = self.config.lr * (-error * q + self.config.lambdaP * p) + self.config.gamma * p_delta[u]
                q_delta[i] = self.config.lr * (-error * p + self.config.lambdaQ * q) + self.config.gamma * q_delta[i]
                self.P[u] -= p_delta[u]  # 更新评分(delta)_Gradient_descent
                self.Q[i] -= q_delta[i]  # 更新评分（delta)_Gradient_descent
            # 最终的目标函数+两项正则项
            self.loss += self.config.lambdaP * (self.P * self.P).sum() + self.config.lambdaQ * (self.Q * self.Q).sum()

            iteration += 1
            if self.isConverged(iteration):  # 判断converge
                iteration = self.config.maxIter  # ？
                break


if __name__ == '__main__':
    # print(bmf.predict_model_cold_users())
    # coldrmse = bmf.predict_model_cold_users()
    # print('cold start user rmse is :' + str(coldrmse))
    # bmf.show_rmse()

    rmses = []
    maes = []
    bmf = FunkSVDwithR(0)
    # print(bmf.rg.trainSet_u[1])
    for i in range(bmf.config.k_fold_num):
        bmf.train_model(i)
        rmse, mae = bmf.predict_model()
        print("current best rmse is %0.5f, mae is %0.5f" % (rmse, mae))
        rmses.append(rmse)
        maes.append(mae)
    rmse_avg = sum(rmses) / 5
    mae_avg = sum(maes) / 5
    print("the rmses are %s" % rmses)
    print("the maes are %s" % maes)
    print("the average of rmses is %s " % rmse_avg)
    print("the average of maes is %s " % mae_avg)
