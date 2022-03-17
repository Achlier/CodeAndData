from reader.rating import RatingGetter
from reader.trust import TrustGetter
from reader.click import ClickGetter
from utility.matrix import SimMatrix
from utility.similarity import *
from utility.tools import *
from configx.configx import ConfigX


class Data:
    def __init__(self, k):
        self.k_current = k
        self.config = ConfigX()

    def get_pearson(self, x1, x2):
        # pearson correlation
        corr = pearson_sp(x1, x2)
        return corr

    def get_SimMatrix(self):
        # similarity Matrix
        return SimMatrix()

    def get_sigmoid_2(self, z):
        #  tools
        return sigmoid_2(z)

    def get_cosine_improved_sp(self, x1, x2):
        # tools
        return cosine_improved_sp(x1, x2)

    def get_cosine(self, x1, x2):
        # similarity
        return cosine(x1, x2)

    def checkRatingBoundary(self, prediction):  # 边界判断，保留3为有效数字（小数）
        prediction = round(min(max(prediction, self.config.min_val), self.config.max_val), 3)
        return prediction

    def read_trust(self, rs):
        rs.tg = TrustGetter(self.config)

    def read_rating(self, rs):
        rs.rg = RatingGetter(self.k_current, rs.config)

    def read_click(self, rs):
        rs.cg = ClickGetter(self.k_current, rs.config)


class RSContext(Data):
    def __repr__(self):
        items = ("%s = %r" % (k, v)
                 for k, v in self.__dict__.items()
                 if not callable(v) and not k.startswith("_"))
        return "Context({%s})" % (', '.join(items),)

    def __init__(self, k):
        super(RSContext, self).__init__(k)
        pass
