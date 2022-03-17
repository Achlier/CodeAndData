# encoding:utf-8
import sys

sys.path.append("..")

import numpy as np
import matplotlib.pylab as plt

from prettyprinter import cpprint
from metrics.metric import Metric
from utility.tools import denormalize, sigmoid
from reader.rating import RatingGetter
from configx.configx import ConfigX


class MF(object):
    """
    docstring for MF
    the base class for matrix factorization based model-parent class

    """

    def __init__(self, k):
        super(MF, self).__init__()  # 继承..
        self.config = ConfigX()  # 初始化config
        self.rg = RatingGetter(k, self.config)
        self.k_current = k
        cpprint(self.config.__dict__)  # print the configuration
        self.P = np.random.rand(self.rg.get_train_size()[0], self.config.factor) / (
                self.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        self.Q = np.random.rand(self.rg.get_train_size()[1], self.config.factor) / (
                self.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        self.loss, self.lastLoss = 0.0, 0.0
        self.lastRmse, self.lastMae = 10.0, 10.0
        # self.rg = RatingGetter()  # loading raing data
        # self.init_model()
        self.iter_rmse = []  # 初始化rmse
        self.iter_mae = []  # 初始化mae
        pass

    def init_model(self, k):
        self.read_data(k)  # self.rg = RatingGetter(k)
        self.P = np.random.rand(self.rg.get_train_size()[0], self.config.factor) / (
                self.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        self.Q = np.random.rand(self.rg.get_train_size()[1], self.config.factor) / (
                self.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        self.loss, self.lastLoss = 0.0, 0.0
        self.lastRmse, self.lastMae = 10.0, 10.0
        pass

    def read_data(self, k):
        self.rg = RatingGetter(k)  # reader/rating.RatingGetter(k)
        pass

    def train_model(self, k):
        self.init_model(k)
        pass

    # test all users in test set
    def predict_model(self, *args):
        res = []
        k = self.k_current
        for ind, entry in enumerate(self.rg.testSet(k)):
            user, item, rating = entry
            rating_length = len(self.rg.trainSet_u[user])  # remove cold start users for test
            if rating_length <= self.config.coldUserRating:
                continue

            prediction = self.predict(user, item)  # 预测-返回一个分数
            # denormalize
            prediction = denormalize(prediction, self.config.min_val, self.config.max_val)  # 0.5 + (x - 0.01) * 3.5

            pred = self.checkRatingBoundary(prediction)  # 对预测值边界进行check, 保留3为小数
            # add prediction in order to measure
            res.append([user, item, rating, pred])  # 加入预测值
        rmse = Metric.RMSE(res)  # sqrt(sum(error**2)/n)
        mae = Metric.MAE(res)  # sum(error=rating-pred)/n
        self.iter_rmse.append(rmse)  # for plot
        self.iter_mae.append(mae)
        return rmse, mae

    # test cold start users among test set
    def predict_model_cold_users(self, *args):  # 用户冷启动
        res = []
        if args:
            rs = args[0]
        for user in self.rg.testColdUserSet_u.keys():  # keys <= 5 启动冷启动 获取user_id
            for item in self.rg.testColdUserSet_u[user].keys():  # 获取对应的item_id
                rating = self.rg.testColdUserSet_u[user][item]  # 获取评分
                pred = self.predict(*args, u=user, i=item)  # 获取预测分
                # pred = sigmoid(pred)
                # denormalize
                pred = denormalize(pred, self.config.min_val, self.config.max_val)  # 去标准化
                pred = self.checkRatingBoundary(pred)  # 检测预测值是否超出评分范围
                res.append([user, item, rating, pred])  # 添加预测值
        rmse = Metric.RMSE(res)  # 计算RMSE
        mae = Metric.MAE(res)  # 计算MAE
        return rmse, mae

    def predict(self,rs, u, i):
        prediction = rs.predict_rs(rs,u,i)
        prediction = self.checkRatingBoundary(prediction)
        pred = denormalize(prediction, self.config.min_val, self.config.max_val)  # 去标准化
        return pred

    def checkRatingBoundary(self, prediction):  # 边界判断，保留3为有效数字（小数）
        prediction = round(min(max(prediction, self.config.min_val), self.config.max_val), 3)
        return prediction

    def isConverged(self, iter):
        from math import isnan
        if isnan(self.loss):  # sum((rating - predict)^2) 这数不应为nan
            print(
                'Loss = NaN or Infinity: current settings does not fit the recommender! Change the settings and try again!')
            exit(-1)

        deltaLoss = (self.lastLoss - self.loss)  # loss 差值
        rmse, mae = self.predict_model()  # 计算rmse mae

        # early stopping
        if self.config.isEarlyStopping == True:  # 确认提早停止
            cond = self.lastRmse < rmse  # 计算是否diverge
            if cond:
                print('test rmse increase, so early stopping')
                return cond
            self.lastRmse = rmse  # 更新lastRmse
            self.lastMae = mae  # 更新lastMae

        print('%s iteration %d: loss = %.4f, delta_loss = %.5f learning_Rate = %.5f rmse=%.5f mae=%.5f' % \
              (self.__class__, iter, self.loss, deltaLoss, self.config.lr, rmse, mae))

        # check if converged
        cond = abs(deltaLoss) < self.config.threshold  # 1e-4
        converged = cond
        # if not converged:
        # 	self.updateLearningRate(iter)
        self.lastLoss = self.loss  # 更新lastLoss
        # shuffle(self.dao.trainingData)
        return converged  # 返回bool

    def updateLearningRate(self, iter):
        if iter > 1:
            if abs(self.lastLoss) > abs(self.loss):
                self.config.lr *= 1.05
            else:
                self.config.lr *= 0.5
        if self.config.lr > 1:
            self.config.lr = 1

    def show_rmse(self):
        '''
        show figure for rmse and epoch
        '''
        nums = range(len(self.iter_rmse))
        plt.plot(nums, self.iter_rmse, label='RMSE')
        plt.plot(nums, self.iter_mae, label='MAE')
        plt.xlabel('# of epoch')
        plt.ylabel('metric')
        plt.title(self.__class__)
        plt.legend()
        plt.show()
        pass

    def show_loss(self, loss_all, faloss_all):
        '''
        show figure for rmse and epoch
        '''
        nums = range(len(loss_all))
        plt.plot(nums, loss_all, label='front')
        plt.plot(nums, faloss_all, label='rear')
        plt.xlabel('# of epoch')
        plt.ylabel('loss')
        plt.title('loss experiment')
        plt.legend()
        plt.show()
        pass

    def init_model_rs(self, rs):
        # rs.P = np.random.rand(rs.get_train_size()[0], rs.config.factor) / (
        #         rs.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        # rs.Q = np.random.rand(rs.get_train_size()[1], rs.config.factor) / (
        #         rs.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        # self.loss, self.lastLoss = 0.0, 0.0
        # self.lastRmse, self.lastMae = 10.0, 10.0
        pass

    def predict_model_rs(self, *args):
        res = []
        rs = args[0]
        if len(args) > 1:
            k = args[1]
        else:
            k = self.k_current
        for ind, entry in enumerate(rs.rg.testSet(k)):
            user, item, rating = entry
            rating_length = len(rs.rg.trainSet_u[user])  # remove cold start users for test
            if rating_length <= rs.rg.config.coldUserRating:
                continue

            prediction = rs.predict_rs(rs, u=user, i=item)  # 预测-返回一个分数
            # denormalize
            prediction = denormalize(prediction, rs.rg.config.min_val, rs.rg.config.max_val)  # 0.5 + (x - 0.01) * 3.5

            pred = self.checkRatingBoundary(prediction)  # 对预测值边界进行check, 保留3为小数
            # add prediction in order to measure
            res.append([user, item, rating, pred])  # 加入预测值
        rmse = Metric.RMSE(res)  # sqrt(sum(error**2)/n)
        mae = Metric.MAE(res)  # sum(error=rating-pred)/n
        self.iter_rmse.append(rmse)  # for plot
        self.iter_mae.append(mae)
        return rmse, mae

    def isConverged_rs(self, iter, *args):
        rs = args[0]
        if len(args) > 1:
            k = args[1]
        else:
            k = self.k_current
        from math import isnan
        if isnan(rs.loss):  # sum((rating - predict)^2) 这数不应为nan
            print(
                'Loss = NaN or Infinity: current settings does not fit the recommender! Change the settings and try again!')
            exit(-1)

        deltaLoss = (self.lastLoss - rs.loss)  # loss 差值
        rmse, mae = self.predict_model_rs(rs, k)  # 计算rmse mae

        # early stopping
        if rs.rg.config.isEarlyStopping == True:  # 确认提早停止
            cond = self.lastRmse < rmse  # 计算是否diverge
            if cond:
                print('test rmse increase, so early stopping')
                return cond
            self.lastRmse = rmse  # 更新lastRmse
            self.lastMae = mae  # 更新lastMae

        print('%s iteration %d: loss = %.4f, delta_loss = %.5f learning_Rate = %.5f rmse=%.5f mae=%.5f' % \
              (rs.__class__, iter, rs.loss, deltaLoss, rs.rg.config.lr, rmse, mae))

        # check if converged
        cond = abs(deltaLoss) < rs.rg.config.threshold  # 1e-4
        converged = cond
        # if not converged:
        # 	self.updateLearningRate(iter)
        self.lastLoss = rs.loss  # 更新lastLoss
        # shuffle(self.dao.trainingData)
        return converged  # 返回bool

    def predict_rs(self, *args, u, i):
        rs = args[0]
        if rs.containsUser(u) and rs.containsItem(i):
            return rs.P[rs.user[u]].dot(rs.Q[rs.item[i]])  # 矩阵相乘user评分*item评分
        elif rs.containsUser(u) and not rs.containsItem(i):
            return rs.userMeans[u]  # 若没有物品评分，则使用用户平均分
        elif not rs.containsUser(u) and rs.containsItem(i):
            return rs.itemMeans[i]  # 若没有用户评分，则使用物品平均分
        else:
            return rs.globalMean  # 若无任何评分(新物品)，则使用所有平均分

    def predict_model_cold_users_rs(self, *args):  # 用户冷启动
        res = []
        rs = args[0]
        for user in rs.rg.testColdUserSet_u.keys():  # keys <= 5 启动冷启动 获取user_id
            for item in rs.rg.testColdUserSet_u[user].keys():  # 获取对应的item_id
                rating = rs.rg.testColdUserSet_u[user][item]  # 获取评分
                pred = rs.predict_rs(rs, u=user, i=item)  # 获取预测分
                # pred = sigmoid(pred)
                # denormalize
                pred = denormalize(pred, self.config.min_val, self.config.max_val)  # 去标准化
                pred = self.checkRatingBoundary(pred)  # 检测预测值是否超出评分范围
                res.append([user, item, rating, pred])  # 添加预测值
        rmse = Metric.RMSE(res)  # 计算RMSE
        mae = Metric.MAE(res)  # 计算MAE
        return rmse, mae
