import TraitData
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import scale
from sklearn.svm import SVR
from permutation_analysis import Permutation
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()


def evaluation_function(model, features, target):
    return -cross_val_score(model, features, target,
                            cv=KFold(5),
                            scoring='neg_mean_squared_error', n_jobs=1).mean()


def SVR_benchmark(datafile, responseVar, drop_features,
                  categorical_features,
                  dropNA, SCORING='neg_mean_squared_error', split=0.30,
                  *algoArgs):
        td = TraitData.TraitData(datafile,
                                 responseVar,
                                 drop_features,
                                 categorical_features,
                                 dropNA=dropNA)
        # get 30% train test split for gridsearch.
        X, x_test, Y, y_test = td.train_test_split(split)

        # Set up SVR  + do grid search

        base = SVR(*algoArgs)

        params_grid = {
            'C': np.logspace(-3, 3, 13),
            'gamma': np.logspace(-3, 3, 13)
        }

        gridSearch = GridSearchCV(base,
                                  param_grid=params_grid,
                                  scoring=SCORING,
                                  error_score=0,
                                  n_jobs=-1,
                                  cv=KFold(5))

        gridSearch.fit(scale(X), Y)

        bestModel = gridSearch.best_estimator_
        # run permutation testing

        return evaluation_function(bestModel, scale(td.X), td.Y)


def evaluation_function(model, features, target):
    return -cross_val_score(model, features, target,
                            cv=KFold(5),
                            scoring='neg_mean_squared_error', n_jobs=1).mean()


def SVR_permutation(datafile, responseVar, drop_features,
                    categorical_features,
                    dropNA,
                    SCORING='neg_mean_squared_error', split=0.30,
                    permutations=1000,
                    threads=20):
        td = TraitData.TraitData(datafile,
                                 responseVar,
                                 drop_features,
                                 categorical_features,
                                 dropNA=dropNA)
        # get 30% train test split for gridsearch.
        X, x_test, Y, y_test = td.train_test_split(split)

        # Set up SVR  + do grid search

        base = SVR()

        params_grid = {
            'C': np.logspace(-3, 3, 13),
            'gamma': np.logspace(-3, 3, 13)
        }

        gridSearch = GridSearchCV(base,
                                  param_grid=params_grid,
                                  scoring=SCORING,
                                  error_score=0,
                                  n_jobs=-1,
                                  cv=KFold(5))

        gridSearch.fit(scale(X), Y)

        bestModel = gridSearch.best_estimator_

        # run permutation testing


        permTester = Permutation(bestModel, scale(td.X), td.Y,
                                 evaluation_function, verbose=True)

        print("Benchmark:", permTester.benchmark())

        permTester.execute_test(n_tests=permutations, threads=threads)
        plot = sns.distplot(permTester.results, rug=True)
        plot.set_xlabel("Mean Squared Error")
        plot.set_ylabel("Probability Density")
        plot.figure.savefig("SVR_permutation_results.png")
        plt.close()

        plot = sns.boxplot(permTester.results)
        plot.figure.savefig("SVR_permutation_box.png")

        print("Benchmark:", permTester.benchmark())
