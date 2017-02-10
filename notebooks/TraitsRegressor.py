import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.model_selection import GridSearchCV



class TraitsRegressor(object):
	"""docstring for TraitsRegressor"""
	def __init__(self, type):
		super(TraitsRegressor, self).__init__()
		self.type = type


		