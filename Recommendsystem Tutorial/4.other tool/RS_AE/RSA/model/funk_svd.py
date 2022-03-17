# encoding:utf-8
import sys

sys.path.append("..")
from model.mf import MF


class FunkSVD(MF):
    """
    docstring for FunkSVD
    implement the FunkSVD without regularization

    http://sifter.org/~simon/journal/20061211.html
    """

    def __init__(self, k):
        super(FunkSVD, self).__init__(k)  # 继承MF
        # self.init_model(0)

    def train_model(self, k):
        super(FunkSVD, self).train_model(k)  # MF.train_model(k) 等价于 MF.init_model(k)
        iteration = 0  # 循环计数
        while iteration < self.config.maxIter:  # 最大循环数，默认100
            self.loss = 0
            for index, line in enumerate(self.rg.trainSet(k)):  # 从训练集获取数据
                user, item, rating = line
                u = self.rg.user[user]  # user对应的index
                i = self.rg.item[item]  # item对应的index
                error = rating - self.predict(u=user, i=item)  # 计算error
                self.loss += error ** 2  # loss = sum((rating - predict)^2)
                p, q = self.P[u], self.Q[i]  # 获取用户/物品行 对应的latent vector
                # update latent vectors
                self.P[u] += self.config.lr * error * q  # p = learning rate * sum(error * q-vector)
                self.Q[i] += self.config.lr * error * p

            iteration += 1
            if self.isConverged(iteration):  # 判断是否Converge
                break


if __name__ == '__main__':

    rmses = []
    bmf = FunkSVD(0)
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
