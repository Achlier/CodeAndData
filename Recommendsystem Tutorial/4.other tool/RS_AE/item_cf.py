import sys

sys.path.append(r'RSA/')
sys.path.append(r'RSA')
from RSA import run_func
import numpy as np


class ItemCf:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        rs.read_rating(rs)
        rs.rg.config.n = 50
        rs.item_sim = rs.get_SimMatrix()
        for i_test in rs.rg.testSet_i:
            for i_train in rs.rg.item:
                if i_train != i_test:
                    if rs.item_sim.contains(i_test, i_train):
                        continue
                    sim = rs.get_pearson(rs.rg.get_col(i_test), rs.rg.get_col(i_train))
                    rs.item_sim.set(i_test, i_train, sim)

    def train_model(self, rs, k):
        pass

    def predict(self, rs, u, i):
        matchItems = sorted(rs.item_sim[i].items(), key=lambda x: x[1], reverse=True)
        itemCount = rs.rg.config.n
        if itemCount > len(matchItems):
            itemCount = len(matchItems)
        sum, denom = 0, 0
        for n in range(itemCount):
            similarItem = matchItems[n][0]
            if rs.rg.containsUserItem(u, similarItem):
                similarity = matchItems[n][1]
                rating = rs.rg.trainSet_u[u][similarItem]
                sum += similarity * (rating - rs.rg.itemMeans[similarItem])
                denom += similarity
        if sum == 0:
            if not rs.rg.containsItem(i):
                return rs.rg.globalMean
            return rs.rg.itemMeans[i]
        pred = rs.rg.itemMeans[i] + sum / float(denom)
        return pred

    def recommend(self, rs, user, num_items=5):
        recommend_dict = {}
        for item in rs.rg.all_Item.keys():
            prediction = self.predict(rs, user, item)  # 预测-返回一个分数
            if item not in rs.rg.trainSet_u[user]:
                recommend_dict[item] = prediction
        recommend_list = sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True)
        return recommend_list[:num_items]
