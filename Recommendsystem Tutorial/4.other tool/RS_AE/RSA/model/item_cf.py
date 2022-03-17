# encoding:utf-8
import sys

sys.path.append("..")
from prettyprinter import cpprint
from model.mf import MF
from utility.matrix import SimMatrix
from utility.similarity import cosine_sp, pearson_sp


class ItemCF(MF):
    """
    docstring for ItemCF
    implement the ItemCF

    Sarwar B, Karypis G, Konstan J, et al. Item-based collaborative filtering recommendation algorithms[C]//Proceedings of the 10th international conference on World Wide Web. ACM, 2001: 285-295.
    """

    def __init__(self, k):
        super(ItemCF, self).__init__(k)  # 继承MF
        self.config.n = 50
        # self.init_model()

    def init_model(self, k):
        super(ItemCF, self).init_model(k)  # MF.init_model(k) 引入self.rg 载入数据
        self.item_sim = SimMatrix()  # 初始化实例矩阵

        for i_test in self.rg.testSet_i:  # 获取测试集 item_id
            for i_train in self.rg.item:  # 获取训练集 item_id
                if i_test != i_train:  # 取不同id
                    if self.item_sim.contains(i_test, i_train):  # 若已经计算过相似度，则跳过
                        continue
                    sim = pearson_sp(self.rg.get_col(i_test), self.rg.get_col(i_train))  # 返回两者相似度
                    self.item_sim.set(i_test, i_train, sim)  # # 构建相似度矩阵(双重dict {i1:{i2:sim,...}},{i2:{i1:sim..}

    def predict(self, u, i):

        # item_sim=dict()
        # for i_train in self.rg.item:
        #     if i != i_train:
        #         if i_train in item_sim :
        #             continue
        #         sim=cosine_sp(self.rg.get_col(i), self.rg.get_col(i_train))
        #         item_sim[i_train]=sim

        matchItems = sorted(self.item_sim[i].items(), key=lambda x: x[1],
                            reverse=True)  # 匹配当前物品i1 和其他物品的相似度{(i2,s1),....}
        itemCount = self.config.n  # 物品表最大长度
        if itemCount > len(matchItems):  # 如果匹配表少于50个
            itemCount = len(matchItems)  # 则降低要求

        sum, denom = 0, 0
        for n in range(itemCount):
            similarItem = matchItems[n][0]  # 获取与当前物品 相似的物品
            if self.rg.containsUserItem(u, similarItem):  # 如果用户u 对相似物品i2有评分
                similarity = matchItems[n][1]  # 获取该相似度
                rating = self.rg.trainSet_u[u][similarItem]  # 获取用户u 对相似物品i2的评分
                sum += similarity * (rating - self.rg.itemMeans[similarItem])  # sum(s*(r-mean of 相似物品评分))
                denom += similarity  # sum(相似度)
        if sum == 0:  # 没有相似物品被u评分 或 其所有相似物品的评分刚好等于其平均分
            if not self.rg.containsItem(i):  # 如果没有物品i 未被u评分
                return self.rg.globalMean  # 返回整体平均值 作为预测值
            return self.rg.itemMeans[i]  # 有物品i，返回i被评分的平均值，作为预测值
        pred = self.rg.itemMeans[i] + sum / float(denom)  # 正常预测值=mean of i + sum(相似度*(r-mean of 相似物品评分))/sum(相似度)
        # print('finished user:'+str(u)+" item:"+str(i))
        return pred
        pass


if __name__ == '__main__':
    ic = ItemCF(k=1)
    ic.init_model(0)
    print(ic.predict_model())
    print(ic.predict_model_cold_users())
    ic.init_model(1)
    print(ic.predict_model())
    print(ic.predict_model_cold_users())
