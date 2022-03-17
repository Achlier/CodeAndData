import sys
sys.path.append(r'../../RScode/RS_AE/RSA')
import os
from reader.rating import RatingGetter
from collections import defaultdict
from utility.tools import  normalize

class RatingGetter_implicit(RatingGetter):
    """
    docstring for RatingGetter
    read rating data and save the global parameters
    """
    def __init__(self, configx, k):
        self.k_current = k  # 引入k
        self.config = configx  # 初始化配置
        self.user = {}
        self.item = {}
        self.all_User = {}
        self.all_Item = {}
        self.id2user = {}
        self.id2item = {}
        self.dataSet_u = defaultdict(dict)
        self.trainSet_u = defaultdict(dict)
        self.trainSet_i = defaultdict(dict)
        self.testSet_u = defaultdict(dict)  # used to store the test set by hierarchy user:[item,rating]
        self.testSet_i = defaultdict(dict)  # used to store the test set by hierarchy item:[user,rating]
        self.testColdUserSet_u = defaultdict(dict)  # cold start users in test set
        self.trainHotUserSet = []  # hot users in train set
        self.trainSetLength = 0
        self.testSetLength = 0

        self.userMeans = {}  # used to store the mean values of users's ratings
        self.itemMeans = {}  # used to store the mean values of items's ratings
        self.globalMean = 0

        self.generate_data_set(k)  # generate train and test set
        self.get_data_statistics()
        self.get_cold_start_users()

    def find_rate(self,x):
        x=float(x)
        if x>=1000:
            return 5
        elif x>=400:
            return 4
        elif x>=200:
            return 3
        elif x>=100:
            return 2
        elif x>=10:
            return 1
        else:
            return 0

    # for cross validation
    def trainSet(self, k):
        # k = self.k_current  # 初始化k值
        for i in range(self.config.k_fold_num):  # k_文件数
            if i != k:  # 非k测试集
                data_path = self.config.rating_cv_path + self.config.dataset_name + "-" + str(i) + ".csv"
                # if not os.path.exists
                if not os.path.isfile(data_path):
                    print("the format of ratings data is wrong!")
                    sys.exit()
                with open(data_path, 'r') as f:  # 读取文件 获取数据
                    for index, line in enumerate(f):
                        u, i, r = line.strip('\r\n').split(self.config.sep)  # ['1.0', '3.0', '3.5']
                        r = normalize(float(self.find_rate(r)))  # scale the rating score to [0-1]
                        yield (int(float(u)), int(float(i)), float(r))  # 将trainSet 做成迭代器

    def testSet(self, k):
        # k = self.k_current  # k为测试集编号
        data_path = self.config.rating_cv_path + self.config.dataset_name + "-" + str(k) + ".csv"
        if not os.path.isfile(data_path):
            print("the format of ratings data is wrong!")
            sys.exit()
        with open(data_path, 'r') as f:  # 读取文件 获取数据
            for index, line in enumerate(f):
                u, i, r = line.strip('\r\n').split(self.config.sep)
                yield (int(float(u)), int(float(i)), float(self.find_rate(r)))  # 将testSet 做成迭代器

