# encoding:utf-8
import sys

sys.path.append("..")
from prettyprinter import cpprint
from model import mf
from utility.matrix import SimMatrix
from utility.similarity import pearson_sp
# test use
from utility.cross_validation import split_5_folds
from configx.configx import ConfigX


class UserCF(mf.MF):
    """
    docstring for UserCF
    implement the UserCF

    Resnick P, Iacovou N, Suchak M, et al. GroupLens: an open architecture for collaborative filtering of netnews[C]//Proceedings of the 1994 ACM conference on Computer supported cooperative work. ACM, 1994: 175-186.
    """

    def __init__(self):
        super(UserCF, self).__init__()  # 继承MF
        self.config.n = 10  # UserCount
        # self.init_model(k)

    def init_model(self, k):
        super(UserCF, self).init_model(k)  # MF.init_model(k) 引入self.rg
        self.user_sim = SimMatrix()  # utility/similarity.SimMatrix()

        for u_test in self.rg.testSet_u:  # testSet_u = {u:{i:r,...},...}
            for u_train in self.rg.user:  # user = {user_id:index} in trainSet
                if u_test != u_train:  # 若用户不同
                    if self.user_sim.contains(u_test, u_train):  # 如果已有两者的相似度，则跳过
                        continue
                    sim = pearson_sp(self.rg.get_row(u_test), self.rg.get_row(u_train))  # 返回两者相似度
                    self.user_sim.set(u_test, u_train, sim)  # 构建相似度矩阵(双重dict {u1:{u2:sim,...}},{u2:{u1:sim..}})

    def predict(self, u, i):  # 在mf.MF.predict_model() 中使用，返回预测值
        matchUsers = sorted(self.user_sim[u].items(), key=lambda x: x[1],
                            reverse=True)  # 匹配当前用户u1 和其他用户的相似度{(u2,s1),....}
        userCount = self.config.n  # n=10,最多匹配10个最接近的用户
        if userCount > len(matchUsers):  # 如果匹配表少于10个
            userCount = len(matchUsers)  # 则将要求降低

        sum, denom = 0, 0
        for n in range(userCount):
            similarUser = matchUsers[n][0]  # 获取与当前用户 相似的用户id
            if self.rg.containsUserItem(similarUser, i):  # 如果 相似用户对物品i有评分
                similarity = matchUsers[n][1]  # 获取两者相似度
                rating = self.rg.trainSet_u[similarUser][i]  # 获取相似用户 对物品i的评分
                sum += similarity * (rating - self.rg.userMeans[similarUser])  # sum(s*(r-mean of 相似用户评分))
                denom += similarity  # sum(相似度)
        if sum == 0:  # 没有相似用户对i有评分 或 其所有相似用户的评分刚好等于其平均分
            if not self.rg.containsUser(u):  # 如果该用户 未对i评分
                return self.rg.globalMean  # 返回所有评分均值 作为预测
            return self.rg.userMeans[u]  # 如果该用户 对i没有评分 返回该用户平均分 作为预测
        pred = self.rg.userMeans[u] + sum / float(denom)  # 正常预测值=mean of u + sum(相似度*(r-mean of 相似用户评分))/sum(相似度)
        return pred


if __name__ == '__main__':
    # test use
    config = ConfigX()
    config.k_fold_num = 5
    config.rating_path = "../data/ft_ratings.txt"
    config.rating_cv_path = "../data/cv/"
    split_5_folds(config)

    uc = UserCF()
    uc.init_model(0)
    print(uc.predict_model())
    print(uc.predict_model_cold_users())
    uc.init_model(1)
    print(uc.predict_model())
    print(uc.predict_model_cold_users())
