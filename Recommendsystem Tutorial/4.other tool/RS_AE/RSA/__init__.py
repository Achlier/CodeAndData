import sys

sys.path.insert(0, "../model")

from model import Main


def run_func(**kwargs):
    user_funcs = {
        'model': kwargs.get('model', None),
        'is_implicit': kwargs.get('is_implicit', None),
    }
    k = 0
    main = Main(k)
    rs = main.run(user_funcs)
    return rs