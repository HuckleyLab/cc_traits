import TraitData
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, train_test_split, cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR 
from permutation_analysis import Permutation
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import numpy as np


datafile = "../data/plants5.csv"

responseVar = "migration_m"

drop_features = ["Taxon",
                 "migr_sterr_m", 
                 "shift + 2SE", 
                 'signif_shift',
                 "signif_shift2",
                 "dispmode01",
                 "DispModeEng", ## what is this
                 "shift + 2SE",
                ]

categorical_features = ["oceanity",
                        "dispersal_mode",
                        "BreedSysCode",
                        "Grime"]

td = TraitData.TraitData(datafile, 
						 responseVar,
						 drop_features,
						 categorical_features, 
						 dropNA = 1)

SCORING = "neg_mean_squared_error"

X, x_test, Y, y_test = td.train_test_split(0.30) ## get 30% train test split for gridsearch. 

### Set up SVR  + do grid search 

base = SVR()

params_grid = {
	'C'     : np.logspace(-3,3,13), 
	'gamma' : np.logspace(-3,3,13)
}

gridSearch = GridSearchCV(base, 
						  param_grid = params_grid, 
						  scoring = SCORING,
						  error_score = 0,
						  n_jobs=-1,
						  cv = KFold(5))

gridSearch.fit(scale(X), Y)	

bestModel = gridSearch.best_estimator_

## run permutation testing

def evaluation_function(model, features, target):
	return -cross_val_score(model, features, target, cv=KFold(5), scoring=SCORING, n_jobs=1).mean()

permTester = Permutation(bestModel, td.X, td.Y, evaluation_function, verbose=True)

permTester.execute_test(n_tests=1000, threads=20)
plot = sns.distplot(permTester.results, rug=True)
plot.set_xlabel("Mean Squared Error")
plot.set_ylabel("Probability Density")
plot.figure.savefig("permutation_results.png")
plt.close()

plot = sns.boxplot(permTester.results)
plot.figure.savefig("permutation_box.png")

print("Benchmark:", permTester.benchmark())




