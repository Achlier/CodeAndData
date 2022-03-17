# encoding:utf-8
import sys

sys.path.append("..")  # add current path into environment variable
import numpy as np
from model.mf import MF
from reader.trust import TrustGetter


# from utility.similarity import pearson_sp


class RSTE(MF):
    """
    docstring for RSTE

    Ma H, King I, Lyu M R. Learning to recommend with social trust ensemble[C]//Proceedings of the 32nd international ACM SIGIR conference on Research and development in information retrieval. ACM, 2009: 203-210.

    """

    def __init__(self):
        super(RSTE, self).__init__()
        # self.maxIter=700
        self.config.alpha = 0.5
        # self.config.lambdaH=0.01
        self.tg = TrustGetter()  # read/trust.py
        # self.init_model()

    def init_model(self, k):
        super(RSTE, self).init_model(k)

    # from collections import defaultdict
    # self.Sim = defaultdict(dict)
    # print('constructing similarity matrix...')
    # for user in self.rg.user:
    # 	for k in self.tg.get_followees(user):
    # 		if user in self.Sim and k in self.Sim[user]:
    # 			pass
    # 		else:
    # 			self.Sim[user][k]=self.get_sim(user,k)

    def train_model(self, k):
        super(RSTE, self).train_model(k)
        iteration = 0
        while iteration < self.config.maxIter:
            self.loss = 0
            for index, line in enumerate(self.rg.trainSet()):
                user, item, rating = line

                error = rating - self.predict(user, item)
                self.loss += error ** 2
                social_term, _ = self.get_social_term_Q(user, item)

                u = self.rg.user[user]
                i = self.rg.item[item]
                p, q = self.P[u], self.Q[i]

                # update latent vectors

                self.P[u] += self.config.lr * (self.config.alpha * error * q + \
                                               (1 - self.config.alpha) * self.get_social_term_P(user,
                                                                                                item) - self.config.lambdaP * p)

                self.Q[i] += self.config.lr * (error * (self.config.alpha * p + (1 - self.config.alpha) * social_term) \
                                               - self.config.lambdaQ * q)

            self.loss += self.config.lambdaP * (self.P * self.P).sum() + self.config.lambdaQ * (self.Q * self.Q).sum()

            iteration += 1
            if self.isConverged(iteration):
                break

    def get_social_term_Q(self, user, item):
        if self.rg.containsUser(user) and self.rg.containsItem(item):
            i = self.rg.item[item]  # item index
            u = self.rg.user[user]  # user index
            social_term_loss = 0
            social_term = np.zeros(self.config.factor)  # vector 1*f
            followees = self.tg.get_followees(user)  # u_from vector 1*m {u_to_1:w,...}
            weights = []
            indexes = []
            for followee in followees:
                if self.rg.containsUser(followee):  # followee is in rating set
                    indexes.append(self.rg.user[followee])  # 有评分的 当前用户关注的用户的index
                    weights.append(followees[followee])  # 比重
            weights = np.array(weights)
            qw = weights.sum()  # 比重总和
            indexes = np.array(indexes)
            if qw != 0:
                social_term = weights.dot(self.P[indexes])  # 返回 vector 1*f
                social_term /= qw  # 加权平均
                social_term_loss += weights.dot((self.P[indexes].dot(self.Q[i]))) / qw  # Sik*Uk^T*Vj
            return social_term, social_term_loss

    def get_social_term_P(self, user, item):
        i = self.rg.item[item]  # item index
        # social_term_loss = 0
        social_term = np.zeros(self.config.factor)  # vector 1*f

        followers = self.tg.get_followers(user) # u_to vector 1*m {u_from_1:w,...}
        weights = []
        indexes = []
        errs = []
        for follower in followers:
            if self.rg.containsUser(follower) and self.rg.containsItem(item) and self.rg.containsUserItem(follower,
                                                                                                          item):  #
                # followee is in rating set
                indexes.append(self.rg.user[follower])  # append u_from index
                weights.append(followers[follower])  # append weight
                errs.append(self.rg.trainSet_u[follower][item] - self.predict(follower, item))  # append error
        weights = np.array(weights)
        indexes = np.array(indexes)
        errs = np.array(errs)
        qw = weights.sum()
        if qw != 0:
            for es in errs * weights:
                social_term += es * self.Q[i]
            social_term /= qw
        # social_term_loss += weights.dot((self.P[indexes].dot(self.Q[i])))
        return social_term

    def predict(self, u, i):
        if self.rg.containsUser(u) and self.rg.containsItem(i):
            _, social_term_loss = self.get_social_term_Q(u, i)
            i = self.rg.item[i]
            u = self.rg.user[u]

            if social_term_loss != 0:
                return self.config.alpha * self.P[u].dot(self.Q[i]) + (1 - self.config.alpha) * social_term_loss
            else:
                return self.P[u].dot(self.Q[i])
        else:
            return self.rg.globalMean

        # def get_sim(self,u,k):
        # 	return (pearson_sp(self.rg.get_row(u), self.rg.get_row(k))+1.0)/2.0


if __name__ == '__main__':
    rmses = []
    maes = []
    tcsr = RSTE()
    # print(bmf.rg.trainSet_u[1])
    for i in range(tcsr.config.k_fold_num):
        print('the %dth cross validation training' % i)
        tcsr.train_model(i)
        rmse, mae = tcsr.predict_model()
        rmses.append(rmse)
        maes.append(mae)
    rmse_avg = sum(rmses) / 5
    mae_avg = sum(maes) / 5
    print("the rmses are %s" % rmses)
    print("the maes are %s" % maes)
    print("the average of rmses is %s " % rmse_avg)
    print("the average of maes is %s " % mae_avg)
