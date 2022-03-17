# encoding:utf-8
import sys

sys.path.append("..")

import pandas as pd
from prettyprinter import cpprint
from configx.configx import ConfigX


class ImplicitMF:
    """
    docstring for ImplicitMF
    the base class for implicit-recomend class

    """

    def __init__(self, k):
        self.k_current = k
        self.config = ConfigX()
        cpprint(self.config.__dict__)
        pass

    def init_model(self, k):
        pass

    def train_model(self, k):
        self.init_model(k)
        pass

    def predict(self, u, i):
        pass

    def recommend(self, rs, user, num_items=10):
        pass
