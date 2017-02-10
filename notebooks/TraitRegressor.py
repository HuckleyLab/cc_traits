import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.model_selection import GridSearchCV

class TraitRegressor(object):
	"""Interface for regression analysis of trait values and evaluation. """
	def __init__(self, regressor, features, target, cvType=None):
		super(TraitsRegressor, self).__init__()
		self.regressor = regressor
		self.gridSearchParams = gridSearchParams
		self.cvType = cvType
		self.features = features
		self.target = target
		self.bestRegressor = None
		self.gridSearchResult = None

	def gridSearch(self, param_grid, scoring, n_jobs=-1, cv=None):
		gridSearch    = GridSearchCV(self.regressor,
									 param_grid = param_grid,
									 scoring=scoring,
									 n_jobs = n_jobs,
									 error_score=0,
									 cv=cv)

		gridSearch.fit(scale(self.features), self.target)
		self.bestRegressor = gridSearch.best_estimator_





		