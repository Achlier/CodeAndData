import sys

sys.path.append(r'RSA')
from RSA import run_func
import numpy as np


class Social_rste:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.alpha = 0.5
        rs.read_rating(rs)
        rs.read_trust(rs)
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

                error = rating - rs.predict_rs(rs, user, item)
                rs.loss += error ** 2
                social_term, _ = self.get_social_term_Q(rs, user, item)

                u = rs.rg.user[user]
                i = rs.rg.item[item]
                p, q = rs.P[u], rs.Q[i]

                # update latent vectors

                rs.P[u] += rs.rg.config.lr * (
                        rs.alpha * error * q +
                        (1 - rs.alpha) * self.get_social_term_P(rs, user, item) -
                        rs.rg.config.lambdaP * p)

                rs.Q[i] += rs.rg.config.lr * (
                        error * (rs.alpha * p +
                                 (1 - rs.alpha) * social_term) -
                        rs.rg.config.lambdaQ * q)

            rs.loss += rs.rg.config.lambdaP * (rs.P * rs.P).sum(
            ) + rs.rg.config.lambdaQ * (rs.Q * rs.Q).sum()

            iteration += 1
            if rs.isConverged_rs(iteration, rs, k):
                break

    def predict(self, rs, u, i):
        if rs.rg.containsUser(u) and rs.rg.containsItem(i):
            _, social_term_loss = self.get_social_term_Q(rs, u, i)
            i = rs.rg.item[i]
            u = rs.rg.user[u]

            if social_term_loss != 0:
                return rs.alpha * rs.P[u].dot(
                    rs.Q[i]) + (1 - rs.alpha) * social_term_loss
            else:
                return rs.P[u].dot(rs.Q[i])
        else:
            return rs.rg.globalMean

    def get_social_term_Q(self, rs, user, item):
        if rs.rg.containsUser(user) and rs.rg.containsItem(item):
            i = rs.rg.item[item]  # item index
            u = rs.rg.user[user]  # user index
            social_term_loss = 0
            social_term = np.zeros(rs.rg.config.factor)  # vector 1*f
            followees = rs.tg.get_followees(
                user)  # u_from vector 1*m {u_to_1:w,...}
            weights = []
            indexes = []
            for followee in followees:
                if rs.rg.containsUser(followee):  # followee is in rating set
                    indexes.append(
                        rs.rg.user[followee])  # 有评分的 当前用户关注的用户的index
                    weights.append(followees[followee])  # 比重
            weights = np.array(weights)
            qw = weights.sum()  # 比重总和
            indexes = np.array(indexes)
            if qw != 0:
                social_term = weights.dot(rs.P[indexes])  # 返回 vector 1*f
                social_term /= qw  # 加权平均
                social_term_loss += weights.dot(
                    (rs.P[indexes].dot(rs.Q[i]))) / qw  # Sik*Uk^T*Vj
            return social_term, social_term_loss

    def get_social_term_P(self, rs, user, item):
        i = rs.rg.item[item]  # item index
        # social_term_loss = 0
        social_term = np.zeros(rs.rg.config.factor)  # vector 1*f

        followers = rs.tg.get_followers(
            user)  # u_to vector 1*m {u_from_1:w,...}
        weights = []
        indexes = []
        errs = []
        for follower in followers:
            if rs.rg.containsUser(follower) and rs.rg.containsItem(
                    item) and rs.rg.containsUserItem(follower, item):  #
                # followee is in rating set
                indexes.append(rs.rg.user[follower])  # append u_from index
                weights.append(followers[follower])  # append weight
                errs.append(rs.rg.trainSet_u[follower][item] -
                            rs.predict_rs(rs, u=follower, i=item))  # append error
        weights = np.array(weights)
        indexes = np.array(indexes)
        errs = np.array(errs)
        qw = weights.sum()
        if qw != 0:
            for es in errs * weights:
                social_term += es * rs.Q[i]
            social_term /= qw
        # social_term_loss += weights.dot((self.P[indexes].dot(self.Q[i])))
        return social_term

    def recommend(self, rs, user, num_items=5):
        recommend_dict = {}
        for item in rs.rg.all_Item.keys():
            prediction = self.predict(rs, user, item)  # 预测-返回一个分数
            if item not in rs.rg.trainSet_u[user]:
                recommend_dict[item] = prediction
        recommend_list = sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True)
        return recommend_list[:num_items]
