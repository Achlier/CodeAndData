from model.mf import MF
from data import RSContext
from configx.configx import ConfigX
from model.implicit_mf import ImplicitMF


class Main:
    def __init__(self, k):
        self.k_current = k
        self.model = None
        self.is_implicit = False

    def read_mf(self, k):
        self.mf = MF(k)

    def read_imf(self, k):
        self.imf = ImplicitMF(k)

    def run(self, user_funcs):
        k = self.k_current
        rs = RSContext(k)
        self.model = user_funcs['model']
        if self.model is None:
            return "None class error!!!!"

        self.is_implicit = user_funcs['is_implicit']
        if self.is_implicit:
            self._run_im(rs, self.model, k)
        else:
            self._run_ex(rs, self.model, k)
        return rs

    def _run_ex(self, rs, model, k):
        self.read_mf(k)
        rs.predict_rs = model.predict
        rs.isConverged_rs = self.mf.isConverged_rs
        model.init_model(rs)
        model.train_model(rs, k)
        rmse, mae = self.mf.predict_model_rs(rs, k)
        rs.estimate = (rmse, mae)
        print(self.mf.predict_model_cold_users_rs(rs))

    def _run_im(self, rs, model, k):
        self.read_imf(k)
        rs.predict = model.predict
        model.init_model(rs)
        model.train_model(rs)
        return rs
