import sys

sys.path.append(r'RSA/')
sys.path.append(r'RSA')
from RSA import run_func
import numpy as np


class SVDPP:
    def __init__(self, factors=10):
        self.factors = factors

    def init_model(self, rs):
        """
        this function is used to initialize the SVD++

        Parameters
        ----------
        rs: rs object from RSA, which is similar to the self and used to deal with data
        """
        rs.lambdaY = 0.001
        rs.lambdaB = 0.001
        rs.config.factor = self.factors
        rs.P = np.random.rand(rs.get_train_size()[0], rs.config.factor) / (
                rs.config.factor ** 0.5)
        rs.Q = np.random.rand(rs.get_train_size()[1], rs.config.factor) / (
                rs.config.factor ** 0.5)
        rs.Bu = np.random.rand(rs.get_train_size()[0]) / (
                rs.config.factor ** 0.5)  # bias value of user
        rs.Bi = np.random.rand(rs.get_train_size()[1]) / (
                rs.config.factor ** 0.5)  # bias value of item
        rs.Y = np.random.rand(rs.get_train_size()[1], rs.config.factor) / (
                rs.config.factor ** 0.5)  # implicit preference
        rs.SY = dict()
        rs.config.maxIter = 160

        def get_sum_y(rs, u):
            """
            this function is used to calculated the sum_y

            Parameters
            ----------
            u: user_id

            Returen
            ----------
            sum_y
            """
            if u in rs.SY:  # 有就直接返回
                return rs.SY[u]
            u_items = rs.user_rated_items(u)  # item_id list
            nu = len(u_items)  # number of items
            sum_y = np.zeros(rs.config.factor)  # factors vector
            for j in u_items:
                sum_y += rs.Y[rs.item[
                    j]]  # item implicit preference of (self.rg.item[j] =) item_j index
            sum_y /= (np.sqrt(nu))  # get mean
            rs.SY[u] = [
                nu, sum_y
            ]  # user_id : [ number of items, item implicit preference ]
            return nu, sum_y

        rs.get_sum_y = get_sum_y

    def train_model(self, rs, k):
        """
        this function is used to train parameters.

        Parameters
        ----------
        k: the test-file data number.
        """
        iteration = 0
        while iteration < rs.config.maxIter:
            rs.loss = 0
            for index, line in enumerate(rs.trainSet(k)):
                user, item, rating = line
                u = rs.user[user]  # u index
                i = rs.item[item]  # i index
                error = rating - rs.predict_rs(rs, u=user, i=item)
                rs.loss += error ** 2

                p, q = rs.P[u], rs.Q[i]
                nu, sum_y = rs.get_sum_y(
                    rs, user)  # number of nei_items, item implicit preference

                # update latent vectors
                rs.P[u] += rs.config.lr * (error * q - rs.config.lambdaP * p)
                rs.Q[i] += rs.config.lr * (error *
                                           (p + sum_y) - rs.config.lambdaQ * q)

                rs.Bu[u] += rs.config.lr * (error - rs.lambdaB * rs.Bu[u])
                rs.Bi[i] += rs.config.lr * (error - rs.lambdaB * rs.Bi[i])

                u_items = rs.user_rated_items(u)
                for j in u_items:
                    idj = rs.item[j]
                    rs.Y[idj] += rs.config.lr * (error / np.sqrt(nu) * q -
                                                 rs.lambdaY * rs.Y[idj])

            rs.loss += rs.config.lambdaP * (rs.P * rs.P).sum(
            ) + rs.config.lambdaQ * (rs.Q * rs.Q).sum() + rs.lambdaB * (
                               (rs.Bu * rs.Bu).sum() +
                               (rs.Bi * rs.Bi).sum()) + rs.lambdaY * (rs.Y *
                                                                      rs.Y).sum()  # get loss
            iteration += 1
            if rs.isConverged_rs(iteration, rs, k):
                break

    def predict(self, rs, u, i):
        """
        this function is used to predict the rating rated by user for item.

        Parameters
        ----------
        u: user_id
        i: item_id

        Returen
        ----------
        predicted rating
        """
        if rs.containsUser(u) and rs.containsItem(i):
            _, sum_y = rs.get_sum_y(rs, u)
            u = rs.user[u]
            i = rs.item[i]
            return rs.Q[i].dot(rs.P[u] + sum_y) + rs.globalMean + rs.Bi[i] + rs.Bu[u]  # 多了个y
        else:
            return rs.globalMean


def recommend(model, user, num_items=5):
    recommend_dict = {}
    for item in model.all_Item.keys():
        prediction = model.predict_rs(model, user, item)  # 预测-返回一个分数
        if item not in model.trainSet_u[user]:
            recommend_dict[item] = prediction
    recommend_list = sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True)
    return recommend_list[:num_items]


def recall_svd(model, num_items=5):
    total_item = 0
    rig_item = 0
    for user in model.all_User.keys():
        item_list = model.testSet_u[user].keys()
        total_item += len(item_list)
        recomm_list = dict(recommend(model, user, num_items)).keys()
        for item in item_list:
            if int(item) in recomm_list:
                rig_item += 1
    return rig_item / total_item


def precision_svd(model, num_items=5):
    total_item = 0
    rig_item = 0
    for user in model.all_User.keys():
        item_list = model.testSet_u[user].keys()
        recomm_list = dict(recommend(model, user, num_items)).keys()
        total_item += len(recomm_list)
        for item in item_list:
            if int(item) in recomm_list:
                rig_item += 1
    return rig_item / total_item
