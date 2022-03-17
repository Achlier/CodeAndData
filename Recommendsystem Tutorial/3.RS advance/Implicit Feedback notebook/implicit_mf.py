import sys
sys.path.append(r'../../RScode/RS_AE/RSA')

import numpy as np
from configx.configx import ConfigX
from model.mf import MF
from prettyprinter import cpprint
from RatingGetter_implicit import RatingGetter_implicit

class implicit_mf(MF):
    def __init__(self,k,data_path):

        configx=ConfigX()
        configx.dataset_name = 'als'
        configx.rating_cv_path = data_path+"/cv/"
        configx.min_val = 0
        configx.max_val = 5

        self.rg = RatingGetter_implicit(configx,k)
        self.k_current = k
        self.config = configx  # 初始化config
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
    
    def read_data(self, k):
        self.rg = RatingGetter_implicit(self.config,k)
        pass
