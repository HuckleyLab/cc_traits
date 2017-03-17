import TraitData
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor
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


def RF_permutation(datafile, responseVar, drop_features,
                   categorical_features,
                   dropNA,
                   SCORING='neg_mean_squared_error', split=0.30,
                   permutations=1000,
                   threads=20):

    td = TraitData.TraitData(datafile, responseVar,
                             drop_features, categorical_features,
                             dropNA=dropNA)

    X, x_test, Y, y_test = td.train_test_split(0.30)

    def importances(weights, features):
        """
        sorts features array based on weights.
        """
        assert(len(weights) == len(features.columns))
        sorted_importances = np.argsort(weights)
        return list(zip(features.columns.values[sorted_importances[::-1]],
                    weights[sorted_importances[::-1]]))

    reg = RandomForestRegressor()

    permTester = Permutation(reg, td.X, td.Y,
                             evaluation_function, verbose=True)
    print("Benchmark:", permTester.benchmark())

    permTester.execute_test(n_tests=1000, threads=40)
    plot = sns.distplot(permTester.results, rug=True)
    plot.set_xlabel("Mean Squared Error")
    plot.set_ylabel("Probability Density")
    plot.figure.savefig("RF_permutation_results.png")
    plt.close()
    plot = sns.boxplot(permTester.results)
    plot.figure.savefig("RF_permutation_box.png")
