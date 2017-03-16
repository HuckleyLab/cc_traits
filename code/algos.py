## algos.py
from sklearn.svm import SVR as scikitSVR
from sklearn.ensemble import RandomForestRegressor as scikitRF
from sklearn.linear_model import LinearRegression as scikitLin
from pyearth import MARS as earthMARS

class SVR(object):
    """docstring for SVR"""
    def __init__(self, *args):
        super(SVR, self).__init__()
        self.regressor = scikitSVR(*args)

        

class RF(object):
    """docstring for RF"""
    def __init__(self, *args):
        super(RF, self).__init__()
        self.regressor = scikitRF(*args)
        

class Linear(object):
    """docstring for Linear"""
    def __init__(self, *args):
        super(Linear, self).__init__()
        self.regressor = scikitLin(*args)
        

class MARS(object):
    """docstring for MARS"""
    def __init__(self, *args):
        super(MARS, self).__init__()
        self.regressor = earthMARS(*args)
        