# encoding:utf-8
import sys

sys.path.append("..")
import os
import pandas as pd
import numpy as np


class ClickGetter:
    """
    docstring for ClickGetter
    read Click count data and save the global parameters
    """

    def __init__(self, k, config):
        self.k_current = k
        self.config = config

        self.train_df = pd.DataFrame()
        self.test_df = pd.DataFrame()

        self.generate_data_frame(k)

    def generate_data_frame(self, k):
        for i in range(self.config.k_fold_num):
            data_path = self.config.rating_cv_path + self.config.dataset_name + "-" + str(i) + ".csv"
            if i != k:
                if not os.path.isfile(data_path):
                    print("the format of ratings data is wrong!")
                    sys.exit()
                else:
                    self.train_df = self.train_df.append(
                        pd.read_csv(data_path, names=['user', 'item', 'clicks'], sep=' ').astype('int'))
            else:
                if not os.path.isfile(data_path):
                    print("the format of ratings data is wrong!")
                    sys.exit()
                else:
                    self.test_df = self.test_df.append(
                        pd.read_csv(data_path, names=['user', 'item', 'clicks'], sep=' ').astype('int'))
