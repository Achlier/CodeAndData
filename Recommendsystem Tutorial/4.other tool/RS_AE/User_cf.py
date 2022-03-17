import sys

sys.path.append(r'RSA/')
sys.path.append(r'RSA')
from RSA import run_func
import numpy as np


class UserCf:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.read_rating(rs)
        rs.rg.config.n = 10
        rs.user_sim = rs.get_SimMatrix()
        for u_test in rs.rg.testSet_u:
            for u_train in rs.rg.user:
                if u_train != u_test:
                    if rs.user_sim.contains(u_test, u_train):
                        continue
                    sim = rs.get_pearson(rs.rg.get_col(u_test), rs.rg.get_col(u_train))
                    rs.user_sim.set(u_test, u_train, sim)

    def train_model(self, rs, k):
        pass

    def predict(self, rs, u, i):
        matchUsers = sorted(rs.user_sim[u].items(), key=lambda x: x[1], reverse=True)
        userCount = rs.rg.config.n
        if userCount > len(matchUsers):
            userCount = len(matchUsers)
        sum, denom = 0, 0
        for n in range(userCount):
            similarUser = matchUsers[n][0]
            if rs.rg.containsUserItem(similarUser, i):
                similarity = matchUsers[n][1]
                rating = rs.rg.trainSet_u[similarUser][i]
                sum += similarity * (rating - rs.rg.userMeans[similarUser])
                denom += similarity
        if sum == 0:
            if not rs.rg.containsUser(u):
                return rs.rg.globalMean
            return rs.rg.userMeans[u]
        pred = rs.rg.userMeans[u] + sum / float(denom)
        return pred

    def recommend(self, rs, user, num_items=5):
        recommend_dict = {}
        for item in rs.rg.all_Item.keys():
            prediction = self.predict(rs, user, item)  # 预测-返回一个分数
            if item not in rs.rg.trainSet_u[user]:
                recommend_dict[item] = prediction
        recommend_list = sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True)
        return recommend_list[:num_items]
