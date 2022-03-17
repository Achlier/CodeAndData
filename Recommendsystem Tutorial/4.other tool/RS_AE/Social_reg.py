import sys

sys.path.append(r'RSA')
from RSA import run_func
import numpy as np


class Social_reg:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.alpha = 0.1
        rs.read_rating(rs)
        rs.read_trust(rs)
        rs.P = np.random.rand(rs.rg.get_train_size()[0], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        rs.Q = np.random.rand(rs.rg.get_train_size()[1], rs.rg.config.factor) / (
                rs.rg.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        rs.user_sim = rs.get_SimMatrix()

        def get_sim(rs, u, k):
            sim = (rs.get_pearson(rs.rg.get_row(u), rs.rg.get_row(k)) +
                   1.0) / 2.0  # fit the value into range [0.0,1.0]
            return sim

        rs.get_sim = get_sim

        for u in rs.rg.user:
            for f in rs.tg.get_followees(u):
                if rs.user_sim.contains(u, f):
                    continue
                sim = rs.get_sim(rs, u, f)  # 计算相似度
                rs.user_sim.set(u, f, sim)  # 记录计算的相似度

    def train_model(self, rs, k):
        iteration = 0
        while iteration < rs.rg.config.maxIter:
            rs.loss = 0
            for index, line in enumerate(rs.rg.trainSet(k)):
                user, item, rating = line
                u = rs.rg.user[user]
                i = rs.rg.item[item]
                error = rating - rs.predict_rs(rs, u=user, i=item)
                rs.loss += 0.5 * error ** 2
                p, q = rs.P[u], rs.Q[i]

                social_term_p, social_term_loss = np.zeros(rs.rg.config.factor), 0.0
                followees = rs.tg.get_followees(
                    user)  # 用户关注(好友)的 set {u_to:w,....}
                for followee in followees:
                    if rs.rg.containsUser(followee):
                        s = rs.user_sim[user][followee]  # 好友的相似度
                        uf = rs.P[rs.rg.user[followee]]  # 好友对应的latent vector
                        social_term_p += s * (p - uf)  # 相似度*(Pu - Pf)
                        social_term_loss += s * ((p - uf).dot(p - uf))

                social_term_m = np.zeros((rs.rg.config.factor))
                followers = rs.tg.get_followers(user)
                for follower in followers:
                    if rs.rg.containsUser(follower):
                        s = rs.user_sim[user][follower]
                        ug = rs.P[rs.rg.user[follower]]
                        social_term_m += s * (p - ug)  # 相似度*(Pu - Pf)

                # update latent vectors
                rs.P[u] += rs.rg.config.lr * (error * q - rs.alpha *
                                              (social_term_p + social_term_m) -
                                              rs.rg.config.lambdaP * p)
                rs.Q[i] += rs.rg.config.lr * (error * p - rs.rg.config.lambdaQ * q)

                rs.loss += 0.5 * rs.alpha * social_term_loss

            rs.loss += 0.5 * rs.rg.config.lambdaP * (rs.P * rs.P).sum(
            ) + 0.5 * rs.rg.config.lambdaQ * (rs.Q * rs.Q).sum()

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
