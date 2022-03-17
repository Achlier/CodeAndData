import numpy as np
import pandas as pd
from math import isnan
from metrics.metric import Metric
from utility.tools import inverse_transform

class implicit_biasSVD:
    """
    docstring for implicit_BiasSVD
    implement the implicit_BiasSVD
    """
   
    def __init__(self):
        pass
        
    def init_model(self ,rs):
        rs.config.dataset_name = 'als'
        rs.read_click(rs)
        rs.cg.train_df['clicks']=inverse_transform(rs.cg.train_df['clicks'])
        rs.iter_rmse = []
        rs.iter_mae = []
        rs.config.lambdaB = 0.001
        rs.cg.user=list(rs.cg.train_df['user'].drop_duplicates())
        rs.cg.item=list(rs.cg.train_df['item'].drop_duplicates())
        rs.cg.get_train_size = (len(rs.cg.train_df['user'].drop_duplicates()),len(rs.cg.train_df['item'].drop_duplicates()))
        rs.P = np.random.rand(rs.cg.get_train_size[0], rs.config.factor) / (
                rs.config.factor ** 0.5)  # latent user matrix 随机初始化 u行,latent列(10)
        rs.Q = np.random.rand(rs.cg.get_train_size[1], rs.config.factor) / (
                rs.config.factor ** 0.5)  # latent item matrix 随机初始化 i行,latent列(10)
        rs.loss, rs.lastLoss = 0.0, 0.0
        rs.lastRmse, rs.lastMae = 10.0, 10.0
        rs.Bu = np.random.rand(rs.cg.get_train_size[0]) / (rs.config.factor ** 0.5)  # bias value of user
        rs.Bi = np.random.rand(rs.cg.get_train_size[1]) / (rs.config.factor ** 0.5)  # bias value of item
        

    def train_model(self ,rs):
        iteration = 0
        while iteration < rs.config.maxIter:
            rs.loss = 0
            for i in range(len(rs.cg.train_df)):
                (user, item, rating) = (rs.cg.train_df.iloc[i,0],rs.cg.train_df.iloc[i,1],rs.cg.train_df.iloc[i,2])
                u = rs.cg.user.index(user)  # index u
                i = rs.cg.item.index(item)  # index i
                error = rating - rs.predict(rs ,user, item)
                rs.loss += error ** 2
                p, q = rs.P[u], rs.Q[i]  # pu qi
                # update latent vectors

                rs.Bu[u] += rs.config.lr * (error - rs.config.lambdaB * rs.Bu[u])  # 更新bias u
                rs.Bi[i] += rs.config.lr * (error - rs.config.lambdaB * rs.Bi[i])  # 更新bias i

                rs.P[u] += rs.config.lr * (error * q - rs.config.lambdaP * p)  # 更新pu
                rs.Q[i] += rs.config.lr * (error * p - rs.config.lambdaQ * q)  # 更新qi

            rs.loss +=rs.config.lambdaP * (rs.P * rs.P).sum() + rs.config.lambdaQ * (rs.Q * rs.Q).sum() \
                         + rs.config.lambdaB * ((rs.Bu * rs.Bu).sum() + (rs.Bi * rs.Bi).sum())
            
            iteration += 1
           
            if self.isConverged(rs ,iteration):
                break

    def isConverged(self, rs, iteration):
        if isnan(rs.loss):  # sum((rating - predict)^2) 这数不应为nan
            print(
                'Loss = NaN or Infinity: current settings does not fit the recommender! Change the settings and try again!')
            exit(-1)

        deltaLoss = (rs.lastLoss - rs.loss)  # loss 差值
        rmse, mae = self.predict_model(rs)  # 计算rmse mae

        # early stopping
        if rs.config.isEarlyStopping == True:  # 确认提早停止
            cond = rs.lastRmse < rmse  # 计算是否diverge
            if cond:
                print('test rmse increase, so early stopping')
                return cond
            rs.lastRmse = rmse  # 更新lastRmse
            rs.lastMae = mae  # 更新lastMae

        print('%s iteration %d: loss = %.4f, delta_loss = %.5f learning_Rate = %.5f rmse=%.5f mae=%.5f' % \
              (self.__class__, iteration, rs.loss, deltaLoss, rs.config.lr, rmse, mae))

        # check if converged
        cond = abs(deltaLoss) < rs.config.threshold  # 1e-4
        converged = cond
        # if not converged:
        rs.lastLoss = rs.loss  # 更新lastLoss
        # shuffle(self.dao.trainingData)
        return converged  # 返回bool
                
                
    def predict_model(self, rs, *args):
        res = []
        k = rs.k_current
        for i in range(len(rs.cg.test_df)):
            (user, item, rating) = (rs.cg.test_df.iloc[i,0],rs.cg.test_df.iloc[i,1],rs.cg.test_df.iloc[i,2])
            rating_length = len(rs.cg.train_df[rs.cg.train_df['user']==user])  # remove cold start users for test
            if rating_length <= rs.config.coldUserRating:
                continue

            prediction = self.predict(rs, user, item)  # 预测-返回一个分数

            pred = self.checkRatingBoundary(rs, prediction)  # 对预测值边界进行check, 保留3为小数
            # add prediction in order to measure
            res.append([user, item, rating, pred])  # 加入预测值
        rmse = Metric.RMSE(res)  # sqrt(sum(error**2)/n)
        mae = Metric.MAE(res)  # sum(error=rating-pred)/n
        rs.iter_rmse.append(rmse)  # for plot
        rs.iter_mae.append(mae)
        return rmse, mae
    
    def checkRatingBoundary(self, rs, prediction):  # 边界判断，保留3为有效数字（小数）
        prediction = round(min(max(prediction, rs.config.min_val), rs.config.max_val), 3)
        return prediction
    
    def predict(self, rs, u, i):
        if u in rs.cg.user and i in rs.cg.item:
            u = rs.cg.user.index(u)  # index u
            i = rs.cg.item.index(i)  # index i
            return rs.P[u].dot(rs.Q[i]) + rs.cg.train_df['clicks'].sum()/len(rs.cg.train_df) + rs.Bi[i] + rs.Bu[u]  # q^T * Pu + u + bu + bi
        else:
            return rs.cg.train_df['clicks'].sum()/len(rs.cg.train_df)
        
    def recommend(self, rs, user, num_items=10):
        item_list=[]
        score_list=[]
        for item in rs.cg.item:
            item_list.append(item)
            score_list.append(self.predict(rs ,user, item))
        recommendations = pd.DataFrame({'artist': item_list, 'score': score_list}).sort_values(by='score', ascending=False)
        return recommendations[:num_items]